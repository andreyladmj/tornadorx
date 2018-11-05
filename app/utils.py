from edusson_ds_main.db.connections import DBConnectionsFacade
from edusson_ds_main.db.models import DashDashboard

analytic_dashboard_id = None


def get_current_dashboard_id(dash_url):
    dashboard_id = None
    dashboard = DBConnectionsFacade.get_edusson_ds_orm_session().query(DashDashboard).filter_by(
        url=dash_url).first()

    if dashboard:
        dashboard_id = dashboard.dashboard_id

    return dashboard_id


def get_analytic_dashboard():
    global analytic_dashboard_id

    if analytic_dashboard_id is None:
        analytic_dashboard_id = get_current_dashboard_id('https://analytics.edusson-data-science.com/dashboard')

    return analytic_dashboard_id
