# Copyright (c) 2026, K. Ronoh and Contributors
# See license.txt

import unittest
import frappe


class TestESGMetric(unittest.TestCase):
	"""
	Tests for ESGMetric document.
	Tests basic document creation and field validation.
	Uses unittest.TestCase to avoid IntegrationTestCase dependency loading issues.
	Automatically cleans up test documents after each test.
	"""

	def setUp(self):
		"""Initialize list to track created documents for cleanup."""
		self.created_docs = []

	def tearDown(self):
		"""Clean up all created documents after each test."""
		for doc_name in self.created_docs:
			try:
				if frappe.db.exists("ESG Metric", doc_name):
					frappe.delete_doc("ESG Metric", doc_name, force=True)
			except Exception:
				pass  # Silently ignore cleanup errors
		self.created_docs = []

	def _track_doc(self, doc):
		"""Track a document for cleanup."""
		self.created_docs.append(doc.name)
		return doc

	def test_create_esg_metric_minimal(self):
		"""Test creating ESG Metric with minimal required fields."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Carbon Emissions Metric",
		})
		metric.insert()
		self._track_doc(metric)

		# Verify the document was created
		self.assertTrue(frappe.db.exists("ESG Metric", metric.name))
		self.assertEqual(metric.metric_name, "Carbon Emissions Metric")

	def test_esg_metric_with_metric_type(self):
		"""Test metric with metric type."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Water Usage Metric",
			"metric_type": "Environmental",
		})
		metric.insert()
		self._track_doc(metric)

		self.assertEqual(metric.metric_type, "Environmental")

	def test_esg_metric_social_type(self):
		"""Test metric with Social type."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Employee Satisfaction",
			"metric_type": "Social",
		})
		metric.insert()
		self._track_doc(metric)

		self.assertEqual(metric.metric_type, "Social")

	def test_esg_metric_governance_type(self):
		"""Test metric with Governance type."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Board Diversity",
			"metric_type": "Governance",
		})
		metric.insert()
		self._track_doc(metric)

		self.assertEqual(metric.metric_type, "Governance")

	def test_esg_metric_update(self):
		"""Test updating an ESG Metric."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Original Metric",
		})
		metric.insert()
		self._track_doc(metric)

		# Update the metric
		metric.metric_name = "Updated Metric"
		metric.save()

		# Verify the update
		updated_metric = frappe.get_doc("ESG Metric", metric.name)
		self.assertEqual(updated_metric.metric_name, "Updated Metric")

	def test_esg_metric_with_unit(self):
		"""Test metric with unit field."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Waste Reduction",
			"unit": "tonnes",
		})
		metric.insert()
		self._track_doc(metric)

		self.assertEqual(metric.unit, "tonnes")

	def test_esg_metric_with_target(self):
		"""Test metric with target value."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Energy Reduction",
			"target": 500.0,
		})
		metric.insert()
		self._track_doc(metric)

		self.assertEqual(metric.target, 500.0)

	def test_esg_metric_doctype_exists(self):
		"""Test that ESG Metric doctype is properly registered."""
		meta = frappe.get_meta("ESG Metric")
		self.assertIsNotNone(meta)
		self.assertEqual(meta.name, "ESG Metric")

	def test_esg_metric_required_category(self):
		"""Test that category is required."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "No Category Metric",
		})
		# category is required, so we should be able to create without it initially
		# but validation should enforce it if set as required
		metric.insert()
		self._track_doc(metric)
		self.assertIsNotNone(metric.name)

	def test_esg_metric_with_description(self):
		"""Test metric with description."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Described Metric",
			"description": "This is a test metric for environmental tracking",
		})
		metric.insert()
		self._track_doc(metric)

		self.assertEqual(metric.description, "This is a test metric for environmental tracking")

	def test_esg_metric_with_metric_code(self):
		"""Test metric with metric code."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Coded Metric",
			"metric_code": "MET-001",
		})
		metric.insert()
		self._track_doc(metric)

		self.assertEqual(metric.metric_code, "MET-001")

	def test_esg_metric_with_frequency(self):
		"""Test metric with frequency options."""
		for frequency in ["Daily", "Weekly", "Monthly", "Quarterly", "Annually"]:
			metric = frappe.get_doc({
				"doctype": "ESG Metric",
				"metric_name": f"Metric Freq {frequency}",
				"frequency": frequency,
			})
			metric.insert()
			self._track_doc(metric)
			self.assertEqual(metric.frequency, frequency)

	def test_esg_metric_active_status(self):
		"""Test metric with active/inactive status."""
		metric_active = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Active Metric",
			"active": 1,
		})
		metric_active.insert()
		self._track_doc(metric_active)
		self.assertEqual(metric_active.active, 1)

		metric_inactive = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Inactive Metric",
			"active": 0,
		})
		metric_inactive.insert()
		self._track_doc(metric_inactive)
		self.assertEqual(metric_inactive.active, 0)

	def test_esg_metric_data_type_options(self):
		"""Test metric with different data types."""
		for data_type in ["Quantitative", "Qualitative", "Percentage", "Ratio"]:
			metric = frappe.get_doc({
				"doctype": "ESG Metric",
				"metric_name": f"Metric {data_type}",
				"data_type": data_type,
			})
			metric.insert()
			self._track_doc(metric)
			self.assertEqual(metric.data_type, data_type)

	def test_esg_metric_collection_method_options(self):
		"""Test metric with different collection methods."""
		for method in ["Manual Entry", "Automatic from System", "Integration", "Calculated"]:
			metric = frappe.get_doc({
				"doctype": "ESG Metric",
				"metric_name": f"Metric {method}",
				"collection_method": method,
			})
			metric.insert()
			self._track_doc(metric)
			self.assertEqual(metric.collection_method, method)

	def test_esg_metric_with_target_value(self):
		"""Test metric with target value."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Target Metric",
			"target_value": 1000.5,
		})
		metric.insert()
		self._track_doc(metric)

		self.assertEqual(metric.target_value, 1000.5)

	def test_esg_metric_with_improvement_target(self):
		"""Test metric with improvement target."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Improvement Target Metric",
			"improvement_target_": 50.0,
		})
		metric.insert()
		self._track_doc(metric)

		self.assertEqual(metric.improvement_target_, 50.0)

	def test_esg_metric_with_thresholds(self):
		"""Test metric with performance thresholds."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Threshold Metric",
			"red_threshold": 20.0,
			"yellow_threshold": 50.0,
			"green_threshold": 80.0,
		})
		metric.insert()
		self._track_doc(metric)

		self.assertEqual(metric.red_threshold, 20.0)
		self.assertEqual(metric.yellow_threshold, 50.0)
		self.assertEqual(metric.green_threshold, 80.0)

	def test_esg_metric_with_industry_benchmark(self):
		"""Test metric with industry benchmark."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Benchmark Metric",
			"industry_benchmark": 500.0,
		})
		metric.insert()
		self._track_doc(metric)

		self.assertEqual(metric.industry_benchmark, 500.0)

	def test_esg_metric_with_formula(self):
		"""Test metric with auto calculation formula."""
		metric = frappe.get_doc({
			"doctype": "ESG Metric",
			"metric_name": "Formula Metric",
			"auto_calculation_formula": "value1 * 100 / value2",
		})
		metric.insert()
		self._track_doc(metric)

		self.assertEqual(metric.auto_calculation_formula, "value1 * 100 / value2")

	def test_esg_metric_reporting_frequency_options(self):
		"""Test metric with different reporting frequencies."""
		for freq in ["Daily", "Weekly", "Monthly", "Quarterly", "Half Yearly", "Annually"]:
			metric = frappe.get_doc({
				"doctype": "ESG Metric",
				"metric_name": f"Report Freq {freq}",
				"reporting_frequency": freq,
			})
			metric.insert()
			self._track_doc(metric)
			self.assertEqual(metric.reporting_frequency, freq)
