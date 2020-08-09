# QML ViewManager

PageManager.qml:
```javascript
import QtQuick 2.5

Item {
    id: viewManager

    property var initialItem
    property var currentItem
    property var items: []

    QtObject {
        id: internal

        property int duration: 500
        property var fadeAnimation: ParallelAnimation {
            running: false

            OpacityAnimator {
                id: fadeInAnimator
                from: 0; to: 1
                duration: internal.duration
            }
            OpacityAnimator {
                id: fadeOutAnimator
                from: 1; to: 0
                duration: internal.duration
            }

            onStopped: {
                internal.transitionEnd(fadeInAnimator.target, fadeOutAnimator.target);
            }
        } //end fadeAnimation

        function transition(enterItem, properties) {
            if (viewManager.currentItem === enterItem) return;

            if (properties && properties.animate === false) {
                transitionEnd(enterItem, viewManager.currentItem);
            } else {
                enterItem.opacity = 0;
                enterItem.visible = true;
                viewManager.currentItem.opacity = 1;
                fadeInAnimator.target = enterItem;
                fadeOutAnimator.target = viewManager.currentItem;
                fadeAnimation.start();
            }
        }

        function transitionEnd(enterItem, exitItem) {
            if (exitItem) {
                exitItem.visible = false;
                exitItem.anchors.fill = undefined;
            }
            viewManager.currentItem = enterItem;
        }
    }//end qtobject

    function transition(itemUrl, properties) {
        for (var i in items) {
            if (items.url === itemUrl) {
                internal.transition(items.object, properties);
                return;
            }
        }

        var component = Qt.createComponent(itemUrl);

        if (component.status === Component.Ready) {
            var item = component.createObject(parent, { "anchors.fill": parent });
            var info = {
                "url": itemUrl,
                "component": component,
                "object": item
            };
            if (!item) items = [];
            items.push(info);
            internal.transition(item, properties);
        } else if (component.status === Component.Error) {
            console.log(component.errorString());
        }
    }

    onInitialItemChanged: {
        if (typeof(initialItem) == "string") {
            transition(initialItem, { "animate": false });
        } else if (typeof(initialItem) == "object") {
            internal.transition(initialItem, { "animate": false });
        }
    }

    onCurrentItemChanged: {
        currentItem.opacity = 1;
        currentItem.visible = true;
    }

    Component.onDestruction: {
        for (var i in items) {
            items.component.destroy();
            items.object.destroy();
        }
    }
}
```
用法:viewManager.transition("xxx.qml", {"xxx": xxx})