import pytest
import datetime
from chains.notice_email_extraction import NoticeEmailExtract

# ✅ Test 1: Ensure all fields are correctly assigned
def test_notice_email_extract_all_fields():
    email_data = NoticeEmailExtract(
        date_of_notice_str="2024-10-15",
        compliance_deadline_str="2024-11-10",
        entity_name="OSHA",
        entity_phone="555-123-4567",
        entity_email="compliance.osha@osha.gov",
        project_id=111232345,
        site_location="Dallas, TX",
        violation_type="Safety Violation",
        required_changes="Install guardrails and fall arrest systems",
        max_potential_fine=25000.0
    )

    # ✅ Check standard fields
    assert email_data.entity_name == "OSHA"
    assert email_data.entity_phone == "555-123-4567"
    assert email_data.entity_email == "compliance.osha@osha.gov"
    assert email_data.project_id == 111232345
    assert email_data.site_location == "Dallas, TX"
    assert email_data.violation_type == "Safety Violation"
    assert email_data.required_changes == "Install guardrails and fall arrest systems"
    assert email_data.max_potential_fine == 25000.0

    # ✅ Check computed date fields
    assert email_data.date_of_notice == datetime.date(2024, 10, 15)
    assert email_data.compliance_deadline == datetime.date(2024, 11, 10)



# ✅ Test 2: Ensure class handles missing fields properly
def test_notice_email_missing_fields():
    email_data = NoticeEmailExtract()
    assert email_data.entity_name is None
    assert email_data.entity_phone is None
    assert email_data.entity_email is None
    assert email_data.project_id is None
    assert email_data.site_location is None
    assert email_data.violation_type is None
    assert email_data.required_changes is None
    assert email_data.max_potential_fine is None
    assert email_data.date_of_notice is None
    assert email_data.compliance_deadline is None




# ✅ Test 3: Partial data should still initialize correctly
def test_notice_email_partial_data():
    email_data = NoticeEmailExtract(entity_name="OSHA", project_id=12345)
    assert email_data.entity_name == "OSHA"
    assert email_data.project_id == 12345
    assert email_data.entity_email is None

