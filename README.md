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
