from ncoreparser import Client, SearchParamWhere, SearchParamType, ParamSort, ParamSeq
import os

# Load environment variables if defined
ncoreuser = os.getenv("ncore_user")
ncorepassword = os.getenv("ncore_password")


client = Client()
client.login(ncoreuser, ncorepassword)

torrent = client.search(pattern="Forrest gump", type=SearchParamType.HD_HUN, number=1,
                            sort_by=ParamSort.SEEDERS, sort_order=ParamSeq.DECREASING)[0]

client.download(torrent, "/tmp")
client.logout()
