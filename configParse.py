import re
import os


class OpenSSHHost():
    def __init__(self, hostname: str, options: dict):

        self.hostname = hostname
        self.options = options

    # def __str__(self):
    #     return f"{str(self.hostname)}: \n   {str(self.options)}"

    def __repr__(self):
        return f"{str(self.hostname)}:  {str(self.options)}"


class OpenSSHConfigParser():

    regexToSplitHosts = re.compile(r"Host *")
    

    optionRegexOptName = "opt_name"
    optionRegexValName = "opt_value"
    regexToMatchOption = re.compile(
        fr"(?P<{optionRegexOptName}>\w+) +(?P<{optionRegexValName}>.+?)\s*$")
    # Regex=re.compile(r"Host *(.+)$\n(.?(\w+) +(.+)$\n)*")

    def _parseConfigFile(self, configFilePath=None):

        if ((configFilePath is None) or not os.path.isfile(configFilePath)):
            raise ValueError("Wrong path")

        with open(configFilePath) as config:
            text = config.read()

            text = text.replace("\t", "")

            hostsInTextList = self.regexToSplitHosts.split(text)

            # print(hostsInTextList)

            hostList = []

            for hostInText in hostsInTextList:
                hostSplited = hostInText.split("\n")
                if len(hostSplited) < 1:
                    continue
                hostname = hostSplited[0]
                options = {}
                for optionString in hostSplited[1:]:

                    optionDict = self.regexToMatchOption.match(optionString)
                    if optionDict:
                        options[optionDict["opt_name"]
                                ] = optionDict["opt_value"]
                    else:
                        print("Skipped:", optionString)

                hostList.append(OpenSSHHost(
                    hostname=hostname, options=options))

        return hostList

    def _parseConfigFolder(self, configFolderPath=None):

        if ((configFolderPath is None) or not os.path.exists(configFolderPath)):
            raise ValueError("Wrong path")



if __name__ == '__main__':

    path = "/home/unknown/.ssh/config.d/rosco.conf"

    print(OpenSSHConfigParser()._parseConfigFile(path))
