from datetime import date, datetime

from .agent_based_api.v1 import *


def discover_k8s_cert_check(section):
    for (
        certificate_issuer,
        certificate_name,
        certificate_expiration_date,
    ) in section:
        certificate_identification = f"{certificate_issuer}/{certificate_name}"
        yield Service(item=certificate_identification)


def check_k8s_cert_check(item, section):
    for (
        certificate_issuer,
        certificate_name,
        certificate_expiration_date,
    ) in section:
        certificate_identification = f"{certificate_issuer}/{certificate_name}"
        if certificate_identification == item:
            expiration_date = datetime.strptime(
                certificate_expiration_date, "%d-%m-%Y"
            ).date()
            current_date = date.today()
            date_difference_delta = expiration_date - current_date
            date_difference_days = int(date_difference_delta.days)

            yield Metric(
                "DAYS_STILL_VALID", date_difference_days, boundaries=(0, None)
            )

            if date_difference_days < 30:
                thought_status = State.CRIT
            elif date_difference_days < 60:
                thought_status = State.WARN
            else:
                thought_status = State.OK

            yield Result(
                state=thought_status,
                summary=f"EXPIRES IN {date_difference_days} DAYS "
                f"ON {certificate_expiration_date}",
            )
            return


register.check_plugin(
    name="k8s_cert_check",
    service_name="K8S certificate - %s",
    discovery_function=discover_k8s_cert_check,
    check_function=check_k8s_cert_check,
)
