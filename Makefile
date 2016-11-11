# file: Makefile	Jiri Spilka (jiri.spilka@ciirc.cvut.cz)

all: MainWindowUI ClinInfoWidgetUI AboutUI ConvertFileUI DataBrowserSelectAttrUI DataBrowserUI DownloadCtuUhbUI AddNoteUI SentAnnotationsUI ExportPdfUI AnnShowHideUI resources

MainWindowUI: MainWindowUI.ui
	pyuic4 MainWindowUI.ui -o MainWindowUI.py

ClinInfoWidgetUI: ClinInfoWidgetUI.ui
	pyuic4 ClinInfoWidgetUI.ui -o ClinInfoWidgetUI.py	

AboutUI: AboutUI.ui
	pyuic4 AboutUI.ui -o AboutUI.py	

ConvertFileUI: ConvertFileUI.ui
	pyuic4 ConvertFileUI.ui -o ConvertFileUI.py	

DataBrowserSelectAttrUI: DataBrowserSelectAttrUI.ui
	pyuic4 DataBrowserSelectAttrUI.ui -o DataBrowserSelectAttrUI.py		

DataBrowserUI: DataBrowserUI.ui
	pyuic4 DataBrowserUI.ui -o DataBrowserUI.py

DownloadCtuUhbUI: DownloadCtuUhbUI.ui
	pyuic4 DownloadCtuUhbUI.ui -o DownloadCtuUhbUI.py	

AddNoteUI: AddNoteUI.ui
	pyuic4 AddNoteUI.ui -o AddNoteUI.py		

SentAnnotationsUI: SentAnnotationsUI.ui
	pyuic4 SentAnnotationsUI.ui -o SentAnnotationsUI.py	

ExportPdfUI: ExportPdfUI.ui
	pyuic4 ExportPdfUI.ui -o ExportPdfUI.py

AnnShowHideUI: AnnShowHideUI.ui
	pyuic4 AnnShowHideUI.ui -o AnnShowHideUI.py	

resources: resources_rc.py resources.qrc
	pyrcc4 resources.qrc -o resources_rc.py
