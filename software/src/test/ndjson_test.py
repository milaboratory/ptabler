import unittest
import os
from ptabler.workflow import PWorkflow
from ptabler.steps import GlobalSettings, ReadCsv, ReadNdjson, WriteCsv, WriteNdjson

current_script_dir = os.path.dirname(os.path.abspath(__file__))
test_data_root_dir = os.path.join(
    os.path.dirname(os.path.dirname(current_script_dir)),
    "test_data")
global_settings = GlobalSettings(root_folder=test_data_root_dir)

class NdjsonTest(unittest.TestCase):

    def test_workflow_read_ndjson_write_csv(self):
        """Test reading NDJSON file and writing to CSV"""
        input_file_relative_path = "test_data_1.ndjson"
        output_file_relative_path = "output_ndjson_to_csv.csv"

        output_file_abs_path = os.path.join(test_data_root_dir, "outputs", output_file_relative_path)

        read_step = ReadNdjson(
            file=input_file_relative_path,
            name="input_table_from_ndjson"
        )

        write_step = WriteCsv(
            table="input_table_from_ndjson",
            file=f"outputs/{output_file_relative_path}",
            columns=["id", "name", "value1", "category"]
        )

        ptw = PWorkflow(workflow=[read_step, write_step])

        if os.path.exists(output_file_abs_path):
            os.remove(output_file_abs_path)

        try:
            ptw.execute(global_settings=global_settings)
            self.assertTrue(os.path.exists(output_file_abs_path),
                            f"Output file was not created at {output_file_abs_path}")

        finally:
            if os.path.exists(output_file_abs_path):
                os.remove(output_file_abs_path)

    def test_workflow_read_csv_write_ndjson(self):
        """Test reading CSV file and writing to NDJSON"""
        input_file_relative_path = "test_data_1.tsv"
        output_file_relative_path = "output_csv_to_ndjson.ndjson"

        output_file_abs_path = os.path.join(test_data_root_dir, "outputs", output_file_relative_path)

        read_step = ReadCsv(
            file=input_file_relative_path,
            name="input_table_from_csv",
            delimiter="\t"
        )

        write_step = WriteNdjson(
            table="input_table_from_csv",
            file=f"outputs/{output_file_relative_path}",
            columns=["id", "name", "value1", "category"]
        )

        ptw = PWorkflow(workflow=[read_step, write_step])

        if os.path.exists(output_file_abs_path):
            os.remove(output_file_abs_path)

        try:
            ptw.execute(global_settings=global_settings)
            self.assertTrue(os.path.exists(output_file_abs_path),
                            f"Output file was not created at {output_file_abs_path}")

        finally:
            if os.path.exists(output_file_abs_path):
                os.remove(output_file_abs_path)

    def test_ndjson_n_rows_functionality(self):
        """Test nRows parameter limits the number of rows read from NDJSON"""
        input_file_relative_path = "test_data_1.ndjson"
        output_file_relative_path = "output_ndjson_limited_rows.csv"

        output_file_abs_path = os.path.join(test_data_root_dir, "outputs", output_file_relative_path)

        read_step = ReadNdjson(
            file=input_file_relative_path,
            name="limited_table_from_ndjson",
            n_rows=3  # Should only read first 3 rows
        )

        write_step = WriteCsv(
            table="limited_table_from_ndjson",
            file=f"outputs/{output_file_relative_path}"
        )

        ptw = PWorkflow(workflow=[read_step, write_step])

        if os.path.exists(output_file_abs_path):
            os.remove(output_file_abs_path)

        try:
            ptw.execute(global_settings=global_settings)
            self.assertTrue(os.path.exists(output_file_abs_path),
                            f"Output file was not created at {output_file_abs_path}")
            
            # Read the output file and verify it has exactly 3 data rows (plus header)
            with open(output_file_abs_path, 'r') as f:
                lines = f.readlines()
                # Should have header + 3 data rows = 4 total lines
                self.assertEqual(len(lines), 4, 
                               f"Expected 4 lines (header + 3 data rows), got {len(lines)}")

        finally:
            if os.path.exists(output_file_abs_path):
                os.remove(output_file_abs_path)

    def test_csv_n_rows_functionality(self):
        """Test nRows parameter limits the number of rows read from CSV"""
        input_file_relative_path = "test_data_1.tsv"
        output_file_relative_path = "output_csv_limited_rows.csv"

        output_file_abs_path = os.path.join(test_data_root_dir, "outputs", output_file_relative_path)

        read_step = ReadCsv(
            file=input_file_relative_path,
            name="limited_table_from_csv",
            delimiter="\t",
            n_rows=2  # Should only read first 2 rows
        )

        write_step = WriteCsv(
            table="limited_table_from_csv",
            file=f"outputs/{output_file_relative_path}"
        )

        ptw = PWorkflow(workflow=[read_step, write_step])

        if os.path.exists(output_file_abs_path):
            os.remove(output_file_abs_path)

        try:
            ptw.execute(global_settings=global_settings)
            self.assertTrue(os.path.exists(output_file_abs_path),
                            f"Output file was not created at {output_file_abs_path}")
            
            # Read the output file and verify it has exactly 2 data rows (plus header)  
            with open(output_file_abs_path, 'r') as f:
                lines = f.readlines()
                # Should have header + 2 data rows = 3 total lines
                self.assertEqual(len(lines), 3, 
                               f"Expected 3 lines (header + 2 data rows), got {len(lines)}")

        finally:
            if os.path.exists(output_file_abs_path):
                os.remove(output_file_abs_path)

    def test_ndjson_roundtrip(self):
        """Test reading NDJSON, writing NDJSON - roundtrip test"""
        input_file_relative_path = "test_data_1.ndjson"
        output_file_relative_path = "output_ndjson_roundtrip.ndjson"

        output_file_abs_path = os.path.join(test_data_root_dir, "outputs", output_file_relative_path)

        read_step = ReadNdjson(
            file=input_file_relative_path,
            name="roundtrip_table"
        )

        write_step = WriteNdjson(
            table="roundtrip_table",
            file=f"outputs/{output_file_relative_path}"
        )

        ptw = PWorkflow(workflow=[read_step, write_step])

        if os.path.exists(output_file_abs_path):
            os.remove(output_file_abs_path)

        try:
            ptw.execute(global_settings=global_settings)
            self.assertTrue(os.path.exists(output_file_abs_path),
                            f"Output file was not created at {output_file_abs_path}")
            
            # Verify the output file has content
            with open(output_file_abs_path, 'r') as f:
                lines = f.readlines()
                self.assertGreater(len(lines), 0, "Output file should not be empty")

        finally:
            if os.path.exists(output_file_abs_path):
                os.remove(output_file_abs_path)

if __name__ == '__main__':
    unittest.main()