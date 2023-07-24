# Java Quarkus Web Application Template

## Dependencies:

- Quarkus Platform
- Extensions:
  - quarkus-agroal                                     Agroal - Database connection pool
  - quarkus-container-image-docker                     Container Image Docker
  - quarkus-container-image-jib                        Container Image Jib
  - quarkus-hibernate-orm-panache                      Hibernate ORM with Panache
  - quarkus-jdbc-h2                                    JDBC Driver - H2
  - quarkus-kubernetes                                 Kubernetes
  - quarkus-micrometer                                 Micrometer metrics
  - quarkus-resteasy-reactive                          RESTEasy Reactive
  - quarkus-resteasy-reactive-jackson                  RESTEasy Reactive Jackson
  - quarkus-resteasy-reactive-qute                     RESTEasy Reactive Qute
  - quarkus-security-jpa                               Security JPA

To test in development mode:
> quarkus dev

To build image(set to Docker in application.properties):
> quarkus build --no-tests

### Docker / Kubernetes

Build process should have automatically loaded image to local repository
> docker image ls

Check for Docker login info for Github repo:
> cat ~/.docker/config.json

Change tag for Github repo:
```
docker image tag LOCALREPO/IMAGE:TAG ghcr.io/USERNAME/IMAGE:TAG
docker push ghcr.io/USERNAME/IMAGE:TAG
```

Make sure credentials in Kubernetes:
```
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=<path/to/.docker/config.json> \
    --type=kubernetes.io/dockerconfigjson
```

Kubernetes YAML file located in ../target/kubernetes/kubernetes.yml

Make sure to change > image: ghcr.io/USERNAME/IMAGE:TAG

So k8s can pull the image from ghcr.io, add this to Deployment:template:spec:
```
imagePullSecrets:
- name: regcred
```

Deploy the webapp to k8s:
> kubectl create -f kubernetes.yml

Check the deployment:
> kubectl get deployments

Check the service:
> kubectl get services -A

To use the native LoadBalancer, change Service:spec:type: ClusterIP => LoadBalancer

To delete the resources:
```
kubectl delete deployment NAME
kubectl delete service NAME
```
