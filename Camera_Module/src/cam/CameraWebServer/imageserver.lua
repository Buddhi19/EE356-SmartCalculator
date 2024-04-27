uart.setup(0, 115200, 8, uart.PARITY_NONE, uart.STOPBITS_1, 0)

while true do
  -- Wait for image size
  local imgSizeBytes = uart.read(0, 4)
  if imgSizeBytes ~= nil then
    local imgSize = string.unpack(">I4", imgSizeBytes)

    -- Read image data
    local imgData = uart.read(0, imgSize)
    if imgData ~= nil then
      -- Process image data here (e.g., display image, save to file, etc.)
      print("Received image data:", imgData)
    end
  end
end
