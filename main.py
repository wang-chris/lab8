import webapp2
import passwords
import MySQLdb
import random
import cgi
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"]="text/html"
        conn=MySQLdb.connect(unix_socket=passwords.SQL_HOST,
                             user = passwords.SQL_USER,
                             passwd = passwords.SQL_PASS,
                             db = 'Lab8')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM webhook;")
        information = cursor.fetchall()
        for i in information:
            self.response.write("<tr><td>'"+str(i[1])+"'</td><td><div><pre>'"+str(i[2])+"'</pre></div></td></tr>")
        conn.close()

    def post(self):
        self.response.headers["Content-Type"]="text/html"
        i = self.request.POST.get('words')
        conn=MySQLdb.connect(unix_socket=passwords.SQL_HOST,
                             user = passwords.SQL_USER,
                             passwd = passwords.SQL_PASS,
                             db = 'Lab8')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO webhook(time, text) VALUES(NOW(),'"+i+"' );")
        conn.commit()
        cursor.execute("SELECT id FROM webhook ORDER BY time;")
        cursor.fetchall()
        length = cursor.rowcount
        if length>20:
            cursor.execute("DELETE FROM webhook LIMIT 1;")
            conn.commit()
        conn.close()
app = webapp2.WSGIApplication([("/", MainPage),], debug=True)