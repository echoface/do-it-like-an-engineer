####FAQ: What's the difference between RenderWidget and RenderView?


      RenderWidget maps to one WebCore::Widget object by implementing the abstract
    interface in the glue layer called WebWidgetDelegate.. 
    This is basically a Window on the screen that receives input events and that we paint into.
    A RenderView inherits from RenderWidget and is the contents of a tab or popup Window.
    It handles navigational commands in addition to the painting and input events of the widget.
    There is only one case where a RenderWidget exists without a RenderView,
    and that's for select boxes on the web page. These are the boxes with the down arrows that pop up a list of options.
    The select boxes must be rendered using a native window so that they can appear above everything else,
    and pop out of the frame if necessary.
    These windows need to paint and receive input, 
    but there isn't a separate "web page" (RenderView) for them.