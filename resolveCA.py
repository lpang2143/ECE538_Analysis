import ssl
import socket


with open("domains.txt", "r") as file:
    domains = file.readlines()
    #domains = ["2 	www-alv.google-analytics.com", "2 	www.amazon.com", "2 	www.espn.com", "2 	www.google-analytics.com", "2 	www.google.com", "2 	www.googleadservices.com", "2 	www.googletagmanager.com", "2 	www.googletagservices.com", "5 	www.gstatic.com", "3 	www.netflix.com", "1 	www.spotify.com", "1 	www.tm.ak.prd.aadg.trafficmanager.net", "2 	www.uniqlo.com"]
    
    filtered_domains = []
    for domain in domains:
        if 'tcp.local' in domain:
            continue
        filtered_domains.append(domain.split()[1])

with open("certificates.txt", "w") as output_file:
    for domain in filtered_domains:
        try:
            # Create a socket and connect to the domain
            sock = socket.create_connection((domain, 443))
            
            # Create an SSL context
            context = ssl.create_default_context()
            
            # Wrap the socket with the SSL context
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                # Get the certificate from the server
                cert = ssock.getpeercert()
                
                # Write the certificate details to the output file
                output_file.write(f"Certificate for {domain}:\n")
                output_file.write(f"Issuer: {cert['issuer']}\n")
                output_file.write(f"Subject: {cert['subject']}\n")
                output_file.write(f"SubjectAltName: {cert['subjectAltName']}\n")
                output_file.write("\n")
                        
        except Exception as e:
            output_file.write(f"Error fetching certificate for {domain}: {e}\n")
            output_file.write("\n")