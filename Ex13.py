import requests
import pytest


class TestEx13:
    userAgents = [({"agent":
                        "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                    "platform": "Mobile",
                    "browser": "No",
                    "device": "Android"}),
                  ({"agent":
                        "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
                    "platform": "Mobile",
                    "browser": "Chrome",
                    "device": "iOS"
                    }),
                  ({"agent":
                        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                    "platform": "Googlebot",
                    "browser": "Unknown",
                    "device": "Unknown"}),
                  ({"agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
                    "platform": "Web",
                    "browser": "Chrome",
                    "device": "No"}),
                  ({"agent":
                        "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                    "platform": "Mobile",
                    "browser": "No",
                    "device": "iPhone"})]

    @pytest.mark.parametrize('userAgent', userAgents)
    def test_checkUserAgent(self, userAgent):
        userAgentName = userAgent.get("agent")
        expectedplatform = userAgent.get("platform")
        expectedbrowser = userAgent.get("browser")
        expecteddevice = userAgent.get("device")

        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        headers = {"User-Agent": userAgentName}

        responseDict = requests.get(url, headers=headers).json()
        actualplatform = responseDict["platform"]
        actualbrowser = responseDict["browser"]
        actualdevice = responseDict["device"]

        assert expectedplatform == actualplatform, f"Incorrect platform. For UserAgent {userAgentName} platform should be {expectedplatform}. Actual platform is {actualplatform}"
        assert expectedbrowser == actualbrowser, f"Incorrect browser. For UserAgent {userAgentName} browser should be {expectedbrowser}. Actual browser is {actualbrowser}"
        assert expecteddevice == actualdevice, f"Incorrect device. For UserAgent {userAgentName} device should be {expecteddevice}. Actual device is {actualdevice}"
