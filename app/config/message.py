import os

from dotenv import load_dotenv
load_dotenv()

class CsgrpmMessage:
    CS_GRP_NAME: str = "CS group name is not given"
    CS_GRP_STATUS: str = "Only 0 or will be accept"
    CS_GRP_STATUS_RES: str = "Only 0 or will be accept in response"
    DELETE_SUCCESS: str = "CS group deleted successfully"
    CS_GRP_SAVE_MESSAGE: str = "CS group name successfully save"
    CS_GRP_LIST_MESSAGE: str = "CS group name list"
    CS_GRP_ACTIVE_LIST_MESSAGE: str = "CS group name active list"
    CS_GRP_UPDATE_MESSAGE: str = "CS group name successfully updated"
    CS_GRP_ID_REQ: str = "Greater than 0 and integer value will be accept in ID"

csgrpmessage = CsgrpmMessage()


class CsmMessage:
    CS_NAME: str = "CS name is not given"
    CS_STATUS: str = "CS status is only 0 or 1"
    CS_GRP_M_ID_MESSAGE: str = "0 or empty value is not acceptable"
    DELETE_SUCCESS: str = "CS deleted successfully"
    CS_SAVE_MESSAGE: str = "CS name successfully save"
    CS_LIST_MESSAGE: str = "CS name list"
    CS_ACTIVE_LIST_MESSAGE: str = "CS name active list"
    CS_UPDATE_MESSAGE: str = "CS name successfully updated"
    CS_GRP_M_ID_NOT_EXIST: str = "Given cs_grp_m_id is not exist"
    
csmmessage = CsmMessage()


class EmpmMessage:
    EMPM_NAME: str = "Emp m name is required"
    EMP_STATUS: str = "emp status is only 0 or 1"
    EMP_M_ID_MESSAGE: str = "0 or empty value is not acceptable"
    EMP_M_PASS_REQUIRED: str = "Password required"
    EMP_M_C_PASS_REQUIRED: str = "Confirm password required"
    PASS_NOT_MATCH: str = "Password and confirm password not match"
    SAVE_SUCCESS: str = "Emp m successfully created"
    EMAIL_DUPLICATE: str = "Duplicate email found"

empm_message = EmpmMessage()

class AuthMessage:
    EMAIL_NOT_EXIST: str = "Email not found"
    INCORRECT_CREDENTIALS: str = "Credential incorrect"
    STATUS_INACTIVE: str = "Inactive employee"
    AUTH_SUCCESSFULL: str = "Login successfull"
    LOGIN_REQUIRED: str = "You have need to login first"

auth_message = AuthMessage()
