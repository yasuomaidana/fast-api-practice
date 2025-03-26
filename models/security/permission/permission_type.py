from enum import Enum


class PermissionType(Enum):
    """
    Attributes:
        READ_INVOICE (str): Permission to read invoices.
        CREATE_INVOICE (str): Permission to create invoices.
        UPDATE_INVOICE (str): Permission to update invoices.
        DELETE_INVOICE (str): Permission to delete invoices.
    """
    READ_INVOICE = "read:invoice"
    CREATE_INVOICE = "create:invoice"
    UPDATE_INVOICE = "update:invoice"
    DELETE_INVOICE = "delete:invoice"
