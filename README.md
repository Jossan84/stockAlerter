# **stockAlerter**

## **Instructions to build Docker containder and run it**

### Build
_docker build --tag stockalerter-dockerization ._

### Run
_docker run -e "EMAIL_USER=$Env:EMAIL_USER" -e "EMAIL_PASS=$Env:EMAIL_PASS" stockalerter-dockerization_