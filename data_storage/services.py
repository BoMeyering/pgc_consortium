"""
Data-storage Service Layers
"""

import csv
from django.http import HttpResponse
from .models import Plot

def export_plots_to_csv(plots):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="plots.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['plot_id', 'plot_label', 'trial_name', 'plot_type', 'block', 'row', 'column', 'parent_plot_id'])

    # Write the data rows
    for plot in plots:
        writer.writerow([plot.db_id, plot.label, plot.trial_id.name, plot.type, plot.block, plot.row, plot.column, plot.parent_plot_id])

    return response
