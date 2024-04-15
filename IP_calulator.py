
def decimal_to_binary (base_decimal_list):
    base_binary_str = ''

    for i_0 in base_decimal_list:
        i_0 = int(i_0)
        element = 0
        i_base_binary = ''
        while i_0 > 0:
            element = i_0 % 2
            i_base_binary += str(element)
            i_0 = i_0 // 2
        if len(i_base_binary) < 8:
            extra_zeros = 8-len(i_base_binary)
            i_base_binary =  i_base_binary + extra_zeros*'0'
        if len(base_binary_str + i_base_binary[::-1]) >31:
            base_binary_str += i_base_binary[::-1] 
        else:
            base_binary_str += i_base_binary[::-1] + '.'
    return base_binary_str

def binary_to_decimal (binary_list):
    decimal_str = ''
    for el in binary_list:
        i = 0
        summary = 0
        for el_0 in el[::-1]:
            increase = int(el_0)*2**i
            i+=1

            summary += increase
            
        if el is binary_list[-1]:
            decimal_str += str(summary) 
        else:
            decimal_str += str(summary) + '.'

    return decimal_str

base_ip_decimal = str(input('Enter IP in decimal: '))
mask_decimal = str(input('Enter mask in decimal: '))

#address IP
base_ip_decimal_list = base_ip_decimal.split('.')
base_ip_binary = decimal_to_binary(base_ip_decimal_list)

#mask
mask_decimal_list = mask_decimal.split('.')
mask_binary = (decimal_to_binary(mask_decimal_list))

#network address
network_address_binary = ''
i = 0
while i<len(mask_binary):
    if mask_binary[i] != '0':
        network_address_binary += base_ip_binary[i]
    else:
        network_address_binary += '0'
    i+=1    
network_address_binary_list = network_address_binary.split('.')
network_address_decimal = binary_to_decimal(network_address_binary_list)

#broadcast address
brodcast_address_binary = ''
i = 0
i_host = 0
while i<len(mask_binary):
    if mask_binary[i] != '0':
        brodcast_address_binary += base_ip_binary[i]
    else:
        brodcast_address_binary += '1'
        i_host += 1
    i+=1    
brodcast_address_binary_list = brodcast_address_binary.split('.')
broadcast_address_decimal = binary_to_decimal(brodcast_address_binary_list)

#number of hosts in the network
number_of_hosts = 2**i_host-2

#host min
host_min_decimal = ''
i = 0
for el in network_address_decimal:
    i+=1
    if i == len(network_address_decimal):
        host_min_decimal += str(int(el)+1)
    else:
        host_min_decimal += el
  
host_min_decimal_list = host_min_decimal.split('.')
host_min_binary = decimal_to_binary(host_min_decimal_list)

#host max
host_max_decimal = ''
i = 0
for el in broadcast_address_decimal:
    i+=1
    if i == len(broadcast_address_decimal):
        host_max_decimal += str(int(el)-1)
    else:
        host_max_decimal +=el
        
host_max_decimal_list = host_max_decimal.split('.')
host_max_binary = decimal_to_binary(host_max_decimal_list)


#exceptions
##########################################################
if mask_decimal == '255.255.255.255':
    print('Adres IP ', base_ip_decimal,'=',base_ip_binary)
    print('Mask',mask_decimal,'=',mask_binary)
elif mask_decimal == '255.255.255.254 ':
    print('Adres IP ', base_ip_decimal,'=',base_ip_binary)
    print('Mask',mask_decimal,'=',mask_binary)
    print('Network address',network_address_decimal,'=',network_address_binary)
    print('Broadcast address',broadcast_address_decimal,'=',brodcast_address_binary)
    print('Number of hostc => point to point')
elif mask_decimal =='0.0.0.0':
    print('Adres IP ', base_ip_decimal,'=',base_ip_binary)
    print('Mask',mask_decimal,'=',mask_binary)
    print('Network address',network_address_decimal,'=',network_address_binary)
    print('Broadcast address',broadcast_address_decimal,'=',brodcast_address_binary)
    print('Number of hosts',number_of_hosts)   
############################################################            
else:
    print('Adres IP ', base_ip_decimal,'=',base_ip_binary)
    print('Mask',mask_decimal,'=',mask_binary)
    print('Network address',network_address_decimal,'=',network_address_binary)
    print('Broadcast address',broadcast_address_decimal,'=',brodcast_address_binary)
    print('Number of hosts',number_of_hosts)
    print('Host min',host_min_decimal,'=',host_min_binary)
    print('Host max',host_max_decimal,'=',host_max_binary)