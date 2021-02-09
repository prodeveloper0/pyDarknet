import pydarknet


img = None
deteoctor = pydarknet.Detector('.cfg', '.weights', '.names')
bbox = deteoctor.detect(img)

