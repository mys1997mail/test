library(rTTRatesHistory)

###Init connection
connection <- ttInitialize(serverName = "cryptottlivewebapi.xbtce.net", port = "8443")
connection_2 <- ttInitialize(serverName = "ttlivewebapi.fxopen.com", port = "8443")

startTime = as.POSIXct("2018-10-11", tz = "GMT")
endTime = as.POSIXct("2018-10-12", tz = "GMT")

###Get Symbols properties
symbols <- connection$GetSymbolsInfo()
symbols_2 <- connection2$GetSymbolsInfo()

###Get Bars History
bars <- connection$GetBarsHistrory("BTCUSD", barsType = "Bid", periodicity = "M1", startTime, endTime)
bars_2 <- connection2$GetBarsHistrory("BTCUSD", barsType = "Bid", periodicity = "M1", startTime, endTime)

###Get Best Ticks History
ticks <- connection$GetTickHistory("BTCUSD", startTime, endTime)
ticks_2 <- connection2$GetTickHistory("EURUSD", startTime, endTime)

###Get Current Ticks
currentQuotes <- connection$GetCurrentQuotes()
currentQuotes_2 <- connection_2$GetCurrentQuotes()

