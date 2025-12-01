# Simple analysis in R, for the program to estimate when it should check if payslip has arrived

dates <- c("Fri, 21 Nov 2025 09:33:43 +0100",
           "Thu, 23 Oct 2025 19:39:04 +0200",
           "Thu, 21 Aug 2025 09:26:34 +0200",
           "Mon, 21 Jul 2025 12:44:56 +0200",
           "Fri, 20 Jun 2025 10:11:00 +0200",
           "Wed, 21 May 2025 10:17:01 +0200",
           "Fri, 18 Apr 2025 09:34:07 +0200",
           "Fri, 21 Mar 2025 10:30:07 +0100",
           "Fri, 21 Feb 2025 11:18:47 +0100",
           "Tue, 21 Jan 2025 10:46:39 +0100",
           "Fri, 13 Dec 2024 11:57:54 +0100",
           "Thu, 21 Nov 2024 11:08:57 +0100",
           "Mon, 21 Oct 2024 10:42:37 +0200",
           "Wed, 21 Aug 2024 12:45:51 +0200",
           "Tue, 21 May 2024 14:12:32 +0200",
           "Fri, 19 Apr 2024 11:06:08 +0200",
           "Thu, 21 Mar 2024 12:56:05 +0100",
           "Wed, 21 Feb 2024 17:54:48 +0100",
           "Fri, 19 Jan 2024 13:33:55 +0100",
           "Thu, 14 Dec 2023 19:05:20 +0100")

# Convert to Date class
dates_parsed <- as.Date(dates, format="%a, %d %b %Y %H:%M:%S %z")

day <- as.integer(format(dates_parsed, "%d"))
month <- as.integer(format(dates_parsed, "%m"))
year <- as.integer(format(dates_parsed, "%Y"))

hist(day, breaks=seq(0,31,1), main="Day of payslip arrival", xlab="Day of Month")


