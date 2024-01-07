from app.applications.domain.repositories import ApplicationRepository
from app.applications.infrastructure.persistence.orm_applications_respository import ORMApplicationRepository


class ApplicationRepositoryFactory:
    _applications_repository = None

    @staticmethod
    def create() -> ApplicationRepository:
        if ApplicationRepositoryFactory._applications_repository is None:
            ApplicationRepositoryFactory._applications_repository = ORMApplicationRepository()

        return ApplicationRepositoryFactory._applications_repository