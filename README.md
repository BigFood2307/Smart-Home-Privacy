# Smart-Home-Privacy
Daten und Skripte zum SES Paper

Die .json Dateien stammen aus einer InfluxDB Datenbank. Bei Abfragen aus dieser erhält man die Daten in der gegebenen JSON Form.
Die Skripte können daher den vorgefertigten JSON-Interpreter von Python nutzen.

Die Lichtschalter Daten wurden aus einem Kalender ausgelesen. Dort werden alle Aktionen um 2 Wochen versetzt abgespeichert, um sie zur Anwesenheitssimulation zu verwenden.
Die zugehörigen Skripte, müssen daher erst alle relvaten Daten aus dem File extrahieren.
