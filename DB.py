import pymysql
import json


def connectToDb():
    db = pymysql.connect(host="10.8.1.34",  # your host, usually localhost
                         user="dbuser",  # your username
                         passwd="atiq99!",  # your password
                         db="designer_db_v0")
    return db


def replaceNoneWithNull(frame):
    for key in frame:
        if frame[key] == None:
            frame[key] = "null"
    return frame


def getChildData(child_id, data):
    child_data = {}
    for item in data:
        if item[0] == child_id:
            child_data = {
                'type': 'create2',
                'object_id': item[2],
                'objectType': item[1],
                'backColor': item[3],
                'frame': replaceNoneWithNull(json.loads(item[4])),
                'children': getChildren(child_id, data)
            }

            if item[1] == 'Image':
                child_data['url'] = item[5]

            if item[1] == 'Label':
                child_data['text'] = item[6]
                child_data['fontSize'] = item[7]

            if item[1] == 'HTMLEditor':
                child_data['text'] = item[6]

            return child_data


def getChildren(parent_id, data):
    childs = []
    db = connectToDb()
    cur = db.cursor()
    sql = "select * from Composition_Items where parent_id = '{}'".format(parent_id)
    cur.execute(sql)
    itemChildren = cur.fetchall()

    for child in itemChildren:
        childs.append(getChildData(child[1], data))
    return childs


def getSingleComposition(report_id, report_name, report_type):
    # Get All data of the report
    db = connectToDb()
    cur = db.cursor()
    sql = "select * from Composition as comp where comp.type_id = '{}'".format(report_id)
    cur.execute(sql)
    result = cur.fetchall()
    canvas = result[0]
    data = {
        'report_name': report_name,
        'report_type': report_type,
        'data': {
            'type': 'create2',
            'object_id': canvas[2],
            'element_id': canvas[2],
            'objectType': canvas[1],
            'backColor': canvas[3],
            'frame': replaceNoneWithNull(json.loads(canvas[4])),
            'children': getChildren(canvas[0], result)
        }
    }

    return data


def getAllCompositions():
    data = []
    db = connectToDb()
    cur = db.cursor()

    # Get specific report_type
    sql = "select * from Type"
    cur.execute(sql)
    reports = cur.fetchall()

    if reports is not None:
        for report in reports:
            data.append(getSingleComposition(report[0], report[1], report[2]))

    return data


def saveReportType(name, type, desc):
    sql = "INSERT INTO Type (Name, Type, Description) VALUES (%s,%s,%s)"
    val = (name, type, desc)

    db = connectToDb()
    cur = db.cursor()
    cur.execute(sql, val)

    db.commit()
    print('Report Saved.')
    return cur.lastrowid


def addToComposition(data):
    sql = "INSERT INTO Composition (Name, Type, Styles, Frame, Image_url, Label_text, Font_size, Creator, Is_private, type_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (data['Name'], data['Type'], data['Styles'], json.dumps(data['Frame']), data['Image_url'], data['Label_text'],
           data['Font_size'], data['Creator'], 0, data['type_id'])

    db = connectToDb()
    cur = db.cursor()
    cur.execute(sql, val)

    db.commit()
    return cur.lastrowid


def addToCompositionItem(child_id, parent_id):
    sql = "INSERT INTO Composition_Items (child_id, parent_id) VALUES (%s, %s)"
    val = (child_id, parent_id)
    db = connectToDb()
    cur = db.cursor()
    cur.execute(sql, val)

    db.commit()


def addToTemplates(name, type, json_data):
    sql = "INSERT INTO Templates (Name, Type, Json_data) VALUES (%s, %s, %s)"
    val = (name, type, json.dumps(json_data))

    db = connectToDb()
    cur = db.cursor()
    cur.execute(sql, val)

    db.commit()
    print('Template added.')


def loadTemplates():
    db = connectToDb()
    cur = db.cursor()
    sql = "select * from Templates"
    cur.execute(sql)
    templates = cur.fetchall()
    return templates


def makeJSON():
    data = getAllCompositions()
    return data
