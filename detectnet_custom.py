import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import sys

Gst.init(None)

# Create a GStreamer pipeline
pipeline = Gst.Pipeline()

# Create elements
source = Gst.ElementFactory.make("nvarguscamerasrc", "camera-source")
convert = Gst.ElementFactory.make("nvvidconv", "converter")
sink = Gst.ElementFactory.make("autovideosink", "video-output")

if not source or not convert or not sink:
    sys.stderr.write("Elements could not be created. Exiting.\n")
    sys.exit(1)

# Set the camera source to csi://0
source.set_property("sensor-id", 0)

# Add elements to the pipeline
pipeline.add(source)
pipeline.add(convert)
pipeline.add(sink)

# Link elements
source.link(convert)
convert.link(sink)

# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

try:
    # Run the main loop
    loop = Gst.MainLoop()
    loop.run()
except KeyboardInterrupt:
    pass
finally:
    # Stop and cleanup
    pipeline.set_state(Gst.State.NULL)
