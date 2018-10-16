import sys
import oersetter.oersetter
import clam.clamservice
application = clam.clamservice.run_wsgi(oersetter.oersetter)
