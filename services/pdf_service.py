from fpdf import FPDF

"""
The PDF class inherits from the FPDF class, which is used to generate pdfs. The goal of the PDF class is to create dynamic tables, which is a 
feature not supported in the fpdf library. It does this by adjusting the width and height to fit the text.
"""
class PDF(FPDF):
    # Creates a dynamic table, where the cell widths and height autofit the text. The data_list is a list of dictionaries.
    def create_dynamic_table(self, data_list):

        headers = list(data_list[0].keys())

        # Extract records from the list of dictionaries
        records = [[str(row.get(header, "")) for header in headers] for row in data_list]

        table = [headers] + records

        column_widths = []
        for col in zip(*table):
            max_width = max(self.get_string_width(str(item)) for item in col) + 4
            column_widths.append(max_width)

        # Get row heights for text
        row_heights = [max( self.get_num_lines(str(cell), col_width) for cell, col_width in zip(row, column_widths))* 5 for row in table]

        # Draw table
        for row_index, row in enumerate(table):
            row_height = row_heights[row_index]

            # Check if the record fits on the current page. If not, add a new page
            if self.get_y() + row_height > self.h - self.b_margin:
                self.add_page() 

            # For each row, we get the cursor position, and then create the border and the cell. Afterwards, we need to set the cursor 
            # position to be after the created cell.
            for col_index, cell in enumerate(row):
                x = self.get_x()
                y = self.get_y()

                # draw border
                self.rect(x, y, column_widths[col_index], row_height)

                # Write the text inside the cell
                self.multi_cell(column_widths[col_index], 5, str(cell), border=0, align="L")

                # Align with the other cell.
                self.set_xy(x + col_widths[col_index], y)

            # Move to the next record
            self.ln(row_height)

    # This function determines how the text in a column fits with the column width. If the text cannot fit inside the cell, then the text
    # should continue on another line.
    def get_num_lines(self, text, width):
        text_width = self.get_string_width(text)
        return int(text_width / width) + 1