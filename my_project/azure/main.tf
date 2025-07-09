provider "azurerm" {
  features {
    
  }
}

resource "azurerm_resource_group" "yonatan_abutbul-rg" {
  name     = "yonatan-resources"
  location = var.location
}

resource "azurerm_virtual_network" "vnet-vnet-yonatan" {
  name                = "yonatan-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = azurerm_resource_group.yonatan_abutbul-rg.name
}

resource "azurerm_subnet" "subnet-yonatan-sb" {
  name                 = "yonatan-subnet"
  resource_group_name  = azurerm_resource_group.yonatan_abutbul-rg.name
  virtual_network_name = azurerm_virtual_network.vnet-vnet-yonatan.name
  address_prefixes     = ["10.0.1.0/24"]
}


resource "azurerm_public_ip" "pip-yonatan-pip" {
  name                = "yonatan-pip"
  location            = var.location
  resource_group_name = azurerm_resource_group.yonatan_abutbul-rg.name
  allocation_method   = "Dynamic"  # Dynamic IP allocation for Basic SKU
  sku = "Basic"  
}

resource "azurerm_network_interface" "nic-yonatan-nic" {
  name                = "yonatan-nic"
  location            = var.location
  resource_group_name = azurerm_resource_group.yonatan_abutbul-rg.name

  ip_configuration {
    name                          = "yonatan-ipconfig"
    subnet_id                     = azurerm_subnet.subnet-yonatan-sb.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.pip-yonatan-pip.id
  }
}


resource "azurerm_linux_virtual_machine" "vm-yonatan_abutbul" {
  name                  = "yonatan-vm"
  location              = var.location
  resource_group_name   = azurerm_resource_group.yonatan_abutbul-rg.name
  network_interface_ids = [azurerm_network_interface.nic-yonatan-nic.id]
  size                  = var.vm_size

  os_disk {
    name              = "yonatan-os-disk"
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  admin_username = var.admin_username
  admin_password = var.admin_password

  disable_password_authentication = false

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  computer_name = "yonatan-vm"
}

resource "time_sleep" "wait_for_ip" {
  create_duration = "120s"
  depends_on = [azurerm_public_ip.pip-yonatan-pip]
}
