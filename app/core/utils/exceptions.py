from dataclasses import dataclass


class AppError(Exception):
    @property
    def message(self) -> str:
        return "An application error occurred"


@dataclass(eq=False)
class UsernameResolverError(AppError):
    username: str


@dataclass(eq=False)
class NoUsernameFound(UsernameResolverError):
    @property
    def message(self) -> str:
        return f"Can't find anything by '@{self.username}'"


@dataclass(eq=False)
class MultipleUsernameFound(UsernameResolverError):
    @property
    def message(self) -> str:
        return f"Exists any users for '@{self.username}'"


@dataclass(eq=False)
class UsernameExist(UsernameResolverError):
    @property
    def message(self) -> str:
        return f"A user with the '{self.username}' username already exists"


@dataclass(eq=False)
class EmailResolverError(AppError):
    email: str


@dataclass(eq=False)
class NoEmailFound(EmailResolverError):
    @property
    def message(self) -> str:
        return f"Can't find anything by '{self.email}'"


@dataclass(eq=False)
class MultipleEmailFound(EmailResolverError):
    @property
    def message(self) -> str:
        return f"Exists any users for '{self.email}'"


@dataclass(eq=False)
class EmailExist(EmailResolverError):
    @property
    def message(self) -> str:
        return f"A user with the '{self.email}' email already exists"


class UnexpectedError(AppError):
    pass


class CommitError(UnexpectedError):
    pass


class RollbackError(UnexpectedError):
    pass


class RepoError(UnexpectedError):
    pass
