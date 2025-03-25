from enum import Enum


class PermissionType(Enum):
    READ_INVOICE = "read:invoice"
    CREATE_INVOICE = "create:invoice"
    UPDATE_INVOICE = "update:invoice"
    DELETE_INVOICE = "delete:invoice"
