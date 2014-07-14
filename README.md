docker-route53
==============

Creates an Amazon Route53 DNS record for the lifetime of a container (deleting the record on stop). Useful for registering the local ec2 instance.

Usage: 

```
docker run -it --rm leg100/route53 \
--name host.example.com. \
--zone example.com. \
--type A. \
--value 123.123.123.123
```

Note: it relies on the ec2 instance possessing an IAM profile, i.e.:

```
{
  "Effect": "Allow",
  "Action": [
    "route53:ChangeResourceRecordSets",
    "route53:GetChange",
    "route53:GetHostedZone",
    "route53:ListResourceRecordSets"
  ],
  "Resource": "arn:aws:route53:::hostedzone/*"
},
{
  "Effect": "Allow",
  "Action": [
    "route53:ListHostedZones"
  ],
  "Resource": "*"
}
```
