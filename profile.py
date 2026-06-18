"""Use this profile to spin up a build machine in OCT."""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab

# Create a Request object to start building the RSpec.
pc = portal.Context()
request = pc.makeRequestRSpec()

# CPU and RAM parameter constraints are removed for bare-metal,
# as you will receive the full unpartitioned resources of the physical node.
toolVersion = ['2023.2', '2023.1'] 

pc.defineParameter("toolVersion", "Tool Version",
                   portal.ParameterType.STRING,
                   toolVersion[0], toolVersion,
                   longDescription="Select the tool version.")    

pc.defineParameter("remoteDesktop", "Remote Desktop Access",
                   portal.ParameterType.BOOLEAN, True,
                   advanced=False,
                   longDescription="Enable remote desktop access by installing GNOME desktop and VNC server.")

params = pc.bindParameters() 
 
# Goal-Driven Execution: Request a RawPC (Bare Metal) instead of a shared XenVM
node = request.RawPC('fpga-tools')
node.component_manager_id = "urn:publicid:IDN+utah.cloudlab.us+authority+cm"
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
node.setFailureAction('nonfatal')
# node.Desire("FPGA-Build-Pool", 1.0)

# The post-boot script execution remains surgically identical
node.addService(pg.Execute(shell="bash", command="sudo /local/repository/post-boot.sh " + str(params.remoteDesktop) + " " + params.toolVersion + " >> /local/logs/output_log.txt"))  

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()
