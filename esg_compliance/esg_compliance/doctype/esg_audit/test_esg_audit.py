# Copyright (c) 2026, K. Ronoh and Contributors
# See license.txt

import unittest
import frappe


class TestESGAudit(unittest.TestCase):
	"""
	Tests for ESGAudit document.
	Tests basic document creation and field validation.
	Uses unittest.TestCase to avoid IntegrationTestCase dependency loading issues.
	"""

	def setUp(self):
		"""Initialize list to track created documents for cleanup."""
		self.created_docs = []

	def tearDown(self):
		"""Clean up all created documents after each test."""
		for doc_name in self.created_docs:
			try:
				if frappe.db.exists("ESG Audit", doc_name):
					frappe.delete_doc("ESG Audit", doc_name, force=True)
			except Exception:
				pass  # Silently ignore cleanup errors
		self.created_docs = []

	def _track_doc(self, doc):
		"""Track a document for cleanup."""
		self.created_docs.append(doc.name)
		return doc

	def test_create_esg_audit_minimal(self):
		"""Test creating ESG Audit with minimal required fields."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Test Audit Minimal",
		})
		audit.insert()
		self._track_doc(audit)

		# Verify the document was created
		self.assertTrue(frappe.db.exists("ESG Audit", audit.name))
		self.assertEqual(audit.audit_name, "Test Audit Minimal")

	def test_esg_audit_autoname_format(self):
		"""Test that ESG Audit uses autoname format correctly."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Autoname Test Audit",
		})
		audit.insert()
		self._track_doc(audit)

		# Verify the autoname format ESG-AUD-YYYY-#####
		self.assertTrue(audit.name.startswith("ESG-AUD-"))

	def test_esg_audit_with_audit_type(self):
		"""Test creating audit with specific audit type."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Typed Audit",
			"audit_type": "Internal",
		})
		audit.insert()
		self._track_doc(audit)

		self.assertEqual(audit.audit_type, "Internal")

	def test_esg_audit_with_status(self):
		"""Test creating audit with status."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Status Audit",
			"status": "Planned",
		})
		audit.insert()

		self.assertEqual(audit.status, "Planned")

	def test_esg_audit_audit_type_external(self):
		"""Test audit with External type."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "External Audit",
			"audit_type": "External",
		})
		audit.insert()

		self.assertEqual(audit.audit_type, "External")

	def test_esg_audit_update_name(self):
		"""Test updating audit name."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Original Name",
		})
		audit.insert()

		# Update the audit
		audit.audit_name = "Updated Name"
		audit.save()

		# Verify the update
		updated_audit = frappe.get_doc("ESG Audit", audit.name)
		self.assertEqual(updated_audit.audit_name, "Updated Name")

	def test_esg_audit_with_audit_scope(self):
		"""Test creating audit with audit scope text."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Scoped Audit",
			"audit_scope": "<p>Review all environmental policies and procedures</p>",
		})
		audit.insert()

		self.assertEqual(audit.audit_scope, "<p>Review all environmental policies and procedures</p>")

	def test_esg_audit_with_recommendations(self):
		"""Test creating audit with recommendations."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Recommendations Audit",
			"recommendations": "<p>Implement renewable energy initiatives</p>",
		})
		audit.insert()

		self.assertEqual(audit.recommendations, "<p>Implement renewable energy initiatives</p>")

	def test_esg_audit_with_overall_rating(self):
		"""Test audit with overall rating options."""
		for rating in ["Excellent", "Good", "Satisfactory", "Needs Improvement", "Poor"]:
			audit = frappe.get_doc({
				"doctype": "ESG Audit",
				"audit_name": f"Audit {rating}",
				"overall_rating": rating,
			})
			audit.insert()
			self.assertEqual(audit.overall_rating, rating)

	def test_esg_audit_certification_type(self):
		"""Test audit with Certification type."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Certification Audit",
			"audit_type": "Certification",
		})
		audit.insert()

		self.assertEqual(audit.audit_type, "Certification")

	def test_esg_audit_regulatory_type(self):
		"""Test audit with Regulatory type."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Regulatory Audit",
			"audit_type": "Regulatory",
		})
		audit.insert()

		self.assertEqual(audit.audit_type, "Regulatory")

	def test_esg_audit_status_ongoing(self):
		"""Test audit with Ongoing status."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Ongoing Audit",
			"status": "Ongoing",
		})
		audit.insert()

		self.assertEqual(audit.status, "Ongoing")

	def test_esg_audit_status_completed(self):
		"""Test audit with Completed status."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Completed Audit",
			"status": "Completed",
		})
		audit.insert()

		self.assertEqual(audit.status, "Completed")

	def test_esg_audit_status_reporting(self):
		"""Test audit with Reporting status."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Reporting Audit",
			"status": "Reporting",
		})
		audit.insert()

		self.assertEqual(audit.status, "Reporting")

	def test_esg_audit_with_audit_date(self):
		"""Test creating audit with audit date."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Dated Audit",
			"audit_date": "2026-01-22",
		})
		audit.insert()

		self.assertEqual(audit.audit_date, "2026-01-22")

	def test_esg_audit_with_next_audit_date(self):
		"""Test creating audit with next audit date."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Next Date Audit",
			"next_audit_date": "2026-07-22",
		})
		audit.insert()

		self.assertEqual(audit.next_audit_date, "2026-07-22")

	def test_esg_audit_with_external_auditor(self):
		"""Test creating audit with external auditor."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "External Audit",
			"external_auditor": "PWC Audit Firm",
		})
		audit.insert()

		self.assertEqual(audit.external_auditor, "PWC Audit Firm")

	def test_esg_audit_delete_and_verify(self):
		"""Test deleting an ESG Audit and verify it's removed."""
		audit = frappe.get_doc({
			"doctype": "ESG Audit",
			"audit_name": "Audit to Delete",
		})
		audit.insert()
		audit_name = audit.name

		# Verify it exists
		self.assertTrue(frappe.db.exists("ESG Audit", audit_name))

		# Delete it
		audit.delete()

		# Verify it's deleted
		self.assertFalse(frappe.db.exists("ESG Audit", audit_name))

	def test_esg_audit_multiple_audits(self):
		"""Test creating multiple ESG Audits."""
		audit_names = []
		for i in range(3):
			audit = frappe.get_doc({
				"doctype": "ESG Audit",
				"audit_name": f"Multi Audit {i}",
				"audit_type": ["Internal", "External", "Certification"][i],
			})
			audit.insert()
			audit_names.append(audit.name)

		# Verify all audits were created
		for audit_name in audit_names:
			self.assertTrue(frappe.db.exists("ESG Audit", audit_name))
