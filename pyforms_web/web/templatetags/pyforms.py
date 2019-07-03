from confapp import conf

from django import template

register = template.Library()

JSFILES_DEBUG = [
    "/static/pyformsjs/ControlBase.js",
    "/static/pyformsjs/ControlAutoComplete.js",
    "/static/pyformsjs/ControlText.js",
    "/static/pyformsjs/ControlTextArea.js",
    "/static/pyformsjs/ControlBreadcrumb.js",
    "/static/pyformsjs/ControlButton.js",
    "/static/pyformsjs/ControlBarsChart.js",
    "/static/pyformsjs/ControlFile.js",
    "/static/pyformsjs/ControlFileUpload.js",
    "/static/pyformsjs/ControlDir.js",
    "/static/pyformsjs/ControlMultipleChecks.js",
    "/static/pyformsjs/ControlMultipleSelection.js",
    "/static/pyformsjs/ControlSlider.js",
    "/static/pyformsjs/ControlCheckBox.js",
    "/static/pyformsjs/ControlCheckBoxList.js",
    "/static/pyformsjs/ControlCheckBoxListQuery.js",
    "/static/pyformsjs/ControlTemplate.js",
    "/static/pyformsjs/ControlCombo.js",
    "/static/pyformsjs/ControlInteger.js",
    "/static/pyformsjs/ControlFloat.js",
    "/static/pyformsjs/ControlCalendar.js",
    "/static/pyformsjs/ControlPieChart.js",
    "/static/pyformsjs/ControlDate.js",
    "/static/pyformsjs/ControlDateTime.js",
    "/static/pyformsjs/ControlImage.js",
    "/static/pyformsjs/ControlImg.js",
    "/static/pyformsjs/ControlHtml.js",
    "/static/pyformsjs/ControlEmail.js",
    "/static/pyformsjs/ControlItemsList.js",
    "/static/pyformsjs/ControlList.js",
    "/static/pyformsjs/ControlLineChart.js",
    "/static/pyformsjs/ControlQueryCombo.js",
    "/static/pyformsjs/ControlQueryList.js",
    "/static/pyformsjs/ControlFeed.js",
    "/static/pyformsjs/ControlQueryCards.js",
    "/static/pyformsjs/ControlPassword.js",
    "/static/pyformsjs/ControlPlayer.js",
    "/static/pyformsjs/ControlPlayerJs.js",
    "/static/pyformsjs/ControlProgress.js",
    "/static/pyformsjs/ControlBoundingSlider.js",
    "/static/pyformsjs/ControlVisVis.js",
    "/static/pyformsjs/ControlLabel.js",
    "/static/pyformsjs/ControlSimpleLabel.js",
    "/static/pyformsjs/ControlTimeout.js",
    "/static/pyformsjs/ControlEmptyWidget.js",
    "/static/pyformsjs/ControlMenu.js",
    "/static/pyformsjs/ControlTree.js",
    "/static/pyformsjs/ControlOrganogram.js",
    "/static/pyformsjs/ControlWorkflow.js",
    "/static/pyformsjs/ControlSearch.js",
    "/static/pyformsjs/BaseWidget.js",
    "/static/pyformsjs/pyforms.js",
    "/static/pyformsjs/pyforms-hub.js",
]
JSFILES_PROD  = [
    "/static/pyforms.js",
]

@register.inclusion_tag('pyforms-dependencies.html')
def pyforms_dependencies():
    return {
        'cssfiles': [
            "/static/pyforms.css",
            "/static/treant/Treant.css",
            "/static/jquery.flowchart/jquery.flowchart.min.css",
            "/static/datetimepicker/jquery.datetimepicker.min.css",
            "/static/jqplot/jquery.jqplot.css",
            "/static/filer/css/jquery.filer.css",
            "/static/filer/css/jquery.filer-dragdropbox-theme.css",
            "/static/semantic-ui/semantic.css",
            "/static/jquery-ui/jquery-ui.min.css"
        ],
        'jsfiles': [
            "/static/jquery.min.js",
            "/static/jquery.json-2.4.min.js",
            "/static/jquery.flowchart/jquery.panzoom.min.js",
            "/static/jquery.flowchart/jquery.mousewheel.min.js",
            "/static/jquery.flowchart/jquery.flowchart.min.js",
            "/static/datetimepicker/jquery.datetimepicker.full.min.js",
            "/static/base64.js",
            "/static/gmaps.min.js",
            "/static/treant/Treant.js",
            "/static/timeline/timeline.js",
            "/static/timeline/track.js",
            "/static/timeline/event.js",
            "/static/timeline/graph.js",
            "/static/canvas-video-player.js",
            "/static/jqplot/jquery.jqplot.js",
            "/static/jqplot/plugins/jqplot.cursor.js",
            "/static/jqplot/plugins/jqplot.logAxisRenderer.js",
            "/static/jqplot/plugins/jqplot.canvasTextRenderer.js",
            "/static/jqplot/plugins/jqplot.canvasAxisLabelRenderer.js",
            "/static/jqplot/plugins/jqplot.blockRenderer.js",
            "/static/jqplot/plugins/jqplot.enhancedLegendRenderer.js",
            "/static/jqplot/plugins/jqplot.logAxisRenderer.js",
            "/static/jqplot/plugins/jqplot.dateAxisRenderer.js",
            "/static/jqplot/plugins/jqplot.categoryAxisRenderer.js",
            "/static/jqplot/plugins/jqplot.barRenderer.js",
            "/static/jqplot/plugins/jqplot.pointLabels.js",
            "/static/jqplot/plugins/jqplot.pieRenderer.js",
            "/static/filer/js/jquery.filer.js",
            "/static/jquery-ui/jquery-ui.min.js",
            "/static/semantic-ui/semantic.min.js",
        ] + (JSFILES_DEBUG if conf.PYFORMS_DEBUG else JSFILES_PROD)
    }
