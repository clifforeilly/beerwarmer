import gdata.docs.service
import gdata.spreadsheet.service


client = gdata.docs.service.DocsService()
client.ClientLogin('clif.com', 'password here')

documents_feed = client.GetDocumentListFeed()

for document_entry in documents_feed.entry:
    print document_entry.title.text


