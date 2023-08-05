=======
PyBoltz
=======

API for authenticating modem users with bolt account::

	from pyboltz.boltz import Boltz

	bolt = Boltz("bolt modem phone number", "password")

	if bolt.authenticate():
		print("authentication success !")
		# profile bolt account
		if bolt.myprofile():
			print(bolt.data_post())
			print(bolt.get_profile())
	else:
		print("authentication failed !")

