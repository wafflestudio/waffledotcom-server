from sqlalchemy.orm import Session

from waffledotcom.src.database.models.sns import SNSAccount
from waffledotcom.src.database.models.user import User


def test_create_sns_account(db_session: Session, sns_account: SNSAccount):
    db_session.add(sns_account)
    db_session.commit()

    sns_accounts = db_session.query(SNSAccount).all()
    assert len(sns_accounts) == 1
    assert sns_accounts[0].name == sns_account.name
    assert sns_accounts[0].url == sns_account.url
    assert sns_accounts[0].user.username == sns_account.user.username


def test_on_delete_sns_account(db_session: Session, sns_account: SNSAccount):
    db_session.add(sns_account)
    db_session.commit()

    db_session.delete(sns_account)
    db_session.commit()

    users = db_session.query(User).all()
    sns_accounts = db_session.query(SNSAccount).all()

    assert len(users) == 1
    assert len(sns_accounts) == 0


def test_on_delete_user_with_sns_account(
    db_session: Session, user: User, sns_account: SNSAccount
):
    user.sns_accounts.append(sns_account)

    db_session.add(user)
    db_session.add(sns_account)
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    users = db_session.query(User).all()
    sns_accounts = db_session.query(SNSAccount).all()

    assert len(users) == 0
    assert len(sns_accounts) == 0


def test_assign_sns_account_to_user(
    db_session: Session, user: User, sns_account: SNSAccount
):
    user.sns_accounts.append(sns_account)

    db_session.add(user)
    db_session.add(sns_account)
    db_session.commit()

    users = db_session.query(User).all()
    sns_accounts = db_session.query(SNSAccount).all()

    assert len(users) == 1
    assert len(sns_accounts) == 1
    assert sns_accounts[0].user.username == user.username
