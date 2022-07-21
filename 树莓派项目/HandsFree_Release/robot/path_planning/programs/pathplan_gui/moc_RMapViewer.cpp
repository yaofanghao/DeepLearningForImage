/****************************************************************************
** Meta object code from reading C++ file 'RMapViewer.h'
**
** Created: Tue May 20 10:55:28 2014
**      by: The Qt Meta Object Compiler version 63 (Qt 4.8.4)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "RMapViewer.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'RMapViewer.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 63
#error "This file was generated using the moc from 4.8.4. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_rtk__RMapViewer[] = {

 // content:
       6,       // revision
       0,       // classname
       0,    0, // classinfo
      11,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: signature, parameters, type, tag, flags
      17,   16,   16,   16, 0x0a,
      26,   16,   16,   16, 0x0a,
      36,   16,   16,   16, 0x0a,
      49,   16,   16,   16, 0x0a,
      71,   16,   16,   16, 0x0a,
      88,   16,   16,   16, 0x0a,
     103,   16,   16,   16, 0x0a,
     122,   16,   16,   16, 0x0a,
     136,   16,   16,   16, 0x0a,
     149,   16,   16,   16, 0x0a,
     162,   16,   16,   16, 0x0a,

       0        // eod
};

static const char qt_meta_stringdata_rtk__RMapViewer[] = {
    "rtk::RMapViewer\0\0zoomIn()\0zoomOut()\0"
    "actMapEdit()\0actMapEditDrawClear()\0"
    "actMapSetBegin()\0actMapSetEnd()\0"
    "actMapClearRoute()\0actMapClear()\0"
    "actMapLoad()\0actMapSave()\0actPathPlanning()\0"
};

void rtk::RMapViewer::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        Q_ASSERT(staticMetaObject.cast(_o));
        RMapViewer *_t = static_cast<RMapViewer *>(_o);
        switch (_id) {
        case 0: _t->zoomIn(); break;
        case 1: _t->zoomOut(); break;
        case 2: _t->actMapEdit(); break;
        case 3: _t->actMapEditDrawClear(); break;
        case 4: _t->actMapSetBegin(); break;
        case 5: _t->actMapSetEnd(); break;
        case 6: _t->actMapClearRoute(); break;
        case 7: _t->actMapClear(); break;
        case 8: _t->actMapLoad(); break;
        case 9: _t->actMapSave(); break;
        case 10: _t->actPathPlanning(); break;
        default: ;
        }
    }
    Q_UNUSED(_a);
}

const QMetaObjectExtraData rtk::RMapViewer::staticMetaObjectExtraData = {
    0,  qt_static_metacall 
};

const QMetaObject rtk::RMapViewer::staticMetaObject = {
    { &QGraphicsView::staticMetaObject, qt_meta_stringdata_rtk__RMapViewer,
      qt_meta_data_rtk__RMapViewer, &staticMetaObjectExtraData }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &rtk::RMapViewer::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *rtk::RMapViewer::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *rtk::RMapViewer::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_rtk__RMapViewer))
        return static_cast<void*>(const_cast< RMapViewer*>(this));
    return QGraphicsView::qt_metacast(_clname);
}

int rtk::RMapViewer::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QGraphicsView::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 11)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 11;
    }
    return _id;
}
QT_END_MOC_NAMESPACE
