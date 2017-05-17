# coding:utf8

from flask_login import UserMixin, AnonymousUserMixin
from fbb.utils.database import CRUDMixin, UTCDateTime
from fbb.utils.helpers import time_utcnow
from fbb.extensions import db, cache


groups_users = db.Table(
    'groups_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer(), db.ForeignKey('groups.id')))


class Group(db.Model, CRUDMixin):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)

    # Group types
    admin = db.Column(db.Boolean, default=False, nullable=False)
    super_mod = db.Column(db.Boolean, default=False, nullable=False)
    mod = db.Column(db.Boolean, default=False, nullable=False)
    guest = db.Column(db.Boolean, default=False, nullable=False)
    banned = db.Column(db.Boolean, default=False, nullable=False)

    # Moderator permissions (only available when the user a moderator)
    mod_edituser = db.Column(db.Boolean, default=False, nullable=False)
    mod_banuser = db.Column(db.Boolean, default=False, nullable=False)

    # User permissions
    editpost = db.Column(db.Boolean, default=True, nullable=False)
    deletepost = db.Column(db.Boolean, default=False, nullable=False)
    deletetopic = db.Column(db.Boolean, default=False, nullable=False)
    posttopic = db.Column(db.Boolean, default=True, nullable=False)
    postreply = db.Column(db.Boolean, default=True, nullable=False)

    # Methods
    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {} {}>".format(self.__class__.__name__, self.id, self.name)


class User(db.Model, UserMixin, CRUDMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    _password = db.Column('password', db.String(120), nullable=False)
    date_joined = db.Column(UTCDateTime(timezone=True), default=time_utcnow)
    lastseen = db.Column(UTCDateTime(timezone=True), default=time_utcnow)
    birthday = db.Column(db.DateTime)
    gender = db.Column(db.String(10))
    website = db.Column(db.String(200))
    location = db.Column(db.String(100))
    signature = db.Column(db.Text)
    avatar = db.Column(db.String(200))
    notes = db.Column(db.Text)

    last_failed_login = db.Column(UTCDateTime(timezone=True))
    login_attempts = db.Column(db.Integer, default=0)
    activated = db.Column(db.Boolean, default=False)

    theme = db.Column(db.String(15))
    language = db.Column(db.String(15), default="en")

    posts = db.relationship("Post", backref="user", lazy="dynamic")
    topics = db.relationship("Topic", backref="user", lazy="dynamic")

    post_count = db.Column(db.Integer, default=0)

    primary_group_id = db.Column(db.Integer, db.ForeignKey('groups.id'),
                                 nullable=False)

    primary_group = db.relationship('Group', lazy="joined",
                                    backref="user_group", uselist=False,
                                    foreign_keys=[primary_group_id])

    secondary_groups = \
        db.relationship('Group',
                        secondary=groups_users,
                        primaryjoin=(groups_users.c.user_id == id),
                        backref=db.backref('users', lazy='dynamic'),
                        lazy='dynamic')

    tracked_topics = \
        db.relationship("Topic", secondary=topictracker,
                        primaryjoin=(topictracker.c.user_id == id),
                        backref=db.backref("topicstracked", lazy="dynamic"),
                        lazy="dynamic")


class Guest(AnonymousUserMixin):
    @property
    def permissions(self):
        return self.get_permissions()

    @property
    def groups(self):
        return self.get_groups()

    @cache.memoize()
    def get_groups(self):
        return Group.query.filter(Group.guest == True).all()

    @cache.memoize()
    def get_permissions(self, exclude=None):
        if exclude:
            exclude = set(exclude)
        else:
            exclude = set()
        exclude.update(["id", "name", "description"])

        perms = {}
        # Get the Guest group
        for group in self.groups:
            columns = set(group.__table__.columns.keys()) - set(exclude)
            for c in columns:
                perms[c] = getattr(group, c) or perms.get(c, False)
        return perms

    @classmethod
    def invalidate_cache(cls):
        """Invalidates this objects cached metadata."""
        cache.delete_memoized(cls.get_permissions, cls)
