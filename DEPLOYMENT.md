# Production Deployment Guide

## Overview

This guide covers deploying InterviewPilot to a production environment with high availability, security, and monitoring.

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] SSL/TLS certificates obtained
- [ ] Monitoring and alerting configured
- [ ] Backup strategy in place
- [ ] Rate limiting configured
- [ ] API documentation updated

## AWS Deployment (Recommended)

### 1. RDS Setup (PostgreSQL)

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier interview-pilot-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --allocated-storage 20 \
  --master-username admin \
  --master-user-password "StrongPassword123!" \
  --backup-retention-period 30 \
  --multi-az
```

### 2. ECR Setup (Docker Registry)

```bash
# Create ECR repository
aws ecr create-repository --repository-name interview-pilot-backend

# Build and push image
docker build -t interview-pilot-backend:latest backend/
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker tag interview-pilot-backend:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/interview-pilot-backend:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/interview-pilot-backend:latest
```

### 3. ECS Deployment

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name interview-pilot

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster interview-pilot \
  --service-name interview-pilot-backend \
  --task-definition interview-pilot-backend \
  --desired-count 2
```

### 4. ALB Setup (Load Balancing)

```bash
# Create load balancer
aws elbv2 create-load-balancer \
  --name interview-pilot-lb \
  --scheme internet-facing \
  --type application

# Create target group
aws elbv2 create-target-group \
  --name interview-pilot-backend \
  --protocol HTTP \
  --port 8000
```

### 5. CloudFront Distribution (Frontend CDN)

```bash
# Create CloudFront distribution
aws cloudfront create-distribution --cli-input-json file://cloudfront-config.json
```

## Health Checks & Monitoring

### CloudWatch Alarms

```bash
# CPU Utilization
aws cloudwatch put-metric-alarm \
  --alarm-name interview-pilot-cpu-high \
  --alarm-description "Alert when CPU > 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold

# Error Rate
aws cloudwatch put-metric-alarm \
  --alarm-name interview-pilot-errors-high \
  --alarm-description "Alert when error rate > 5%" \
  --metric-name ErrorRate \
  --namespace InterviewPilot \
  --statistic Average \
  --period 60 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold
```

## Database Migrations

```bash
# Run migrations on production database
export DATABASE_URL="postgresql://user:pass@prod-db.rds.amazonaws.com:5432/interview_pilot"
python -m alembic upgrade head
```

## Backup Strategy

### Automated RDS Backups

```bash
# Enable automated backups
aws rds modify-db-instance \
  --db-instance-identifier interview-pilot-db \
  --backup-retention-period 30 \
  --preferred-backup-window "03:00-04:00"
```

### Manual Snapshots

```bash
# Create manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier interview-pilot-db \
  --db-snapshot-identifier interview-pilot-backup-$(date +%Y%m%d)
```

## SSL/TLS Setup

```bash
# Request certificate from ACM
aws acm request-certificate \
  --domain-name interviewpilot.com \
  --validation-method DNS

# Validate domain and attach to ALB
aws elbv2 modify-listener \
  --listener-arn <listener-arn> \
  --protocol HTTPS \
  --certificates CertificateArn=<cert-arn>
```

## Scaling Configuration

### Auto Scaling Group

```bash
# Create launch template
aws ec2 create-launch-template \
  --launch-template-name interview-pilot-template \
  --version-description "InterviewPilot backend" \
  --launch-template-data '{...}'

# Create auto scaling group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name interview-pilot-asg \
  --launch-template LaunchTemplateName=interview-pilot-template \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 2 \
  --health-check-type ELB \
  --health-check-grace-period 300
```

## Log Aggregation (CloudWatch Logs)

```bash
# Create log group
aws logs create-log-group --log-group-name /aws/ecs/interview-pilot

# Create log stream
aws logs create-log-stream \
  --log-group-name /aws/ecs/interview-pilot \
  --log-stream-name backend
```

## Security Best Practices

1. **VPC Configuration**
   - Place RDS in private subnet
   - Use security groups to restrict access
   - Enable VPC Flow Logs

2. **Secrets Management**
   - Use AWS Secrets Manager for API keys
   - Rotate credentials regularly
   - Never commit secrets to git

3. **IAM Policies**
   - Principle of least privilege
   - Use roles instead of access keys
   - Enable MFA for admin access

4. **DDoS Protection**
   - Enable AWS Shield
   - Configure WAF rules
   - Use CloudFlare or similar CDN

## Performance Optimization

### Database Optimization

```sql
-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_interviews_user_id ON interviews(user_id);
CREATE INDEX idx_user_memory_user_id ON user_memory(user_id);

-- Vacuum and analyze
VACUUM ANALYZE;
```

### Caching Strategy

```python
# Use Redis for caching
import redis

cache = redis.Redis(
    host='interview-pilot-redis.xxxxx.ng.0001.use1.cache.amazonaws.com',
    port=6379,
    db=0
)

# Cache research results
cache.setex(f'research:{company}:{role}', 86400, json.dumps(research_data))
```

### CDN Configuration

```javascript
// CloudFront headers for frontend
{
  "CacheBehaviors": [
    {
      "PathPattern": "/api/*",
      "CachePolicyId": "4135ea3d-c35d-46eb-81d7-reeff432cf88",
      "OriginRequestPolicyId": "216adef5-5c7f-47e4-b989-5492eafa07d3"
    }
  ]
}
```

## Monitoring Dashboard

### Custom CloudWatch Dashboard

```bash
aws cloudwatch put-dashboard \
  --dashboard-name InterviewPilot \
  --dashboard-body file://dashboard-config.json
```

## Disaster Recovery

### RTO: 30 minutes | RPO: 5 minutes

1. **Backup Verification**
   - Test restore from latest snapshot weekly
   - Maintain backup in separate region

2. **Failover Procedure**
   - Promote read replica to master
   - Update DNS to failover endpoint
   - Notify users of incident

3. **Communication Plan**
   - Status page updates
   - Email notifications
   - Social media updates

## Cost Optimization

- Use reserved instances for predictable workloads
- Implement auto-scaling to handle variable traffic
- Use S3 Glacier for long-term backups
- Monitor and optimize data transfer costs

## Rollback Procedure

```bash
# If deployment fails, rollback to previous version
aws ecs update-service \
  --cluster interview-pilot \
  --service interview-pilot-backend \
  --task-definition interview-pilot-backend:PREVIOUS_VERSION

# Monitor rollback
aws ecs describe-services \
  --cluster interview-pilot \
  --services interview-pilot-backend
```

---

For issues or support during production deployment, contact: devops@interviewpilot.com
