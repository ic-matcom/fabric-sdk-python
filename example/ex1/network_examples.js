	const channel_name = 'mychannel2';
	// build a 'Client' instance that knows the connection profile
	//  this connection profile does not have the client information, we will
	//  load that later so that we can switch this client to be in a different
	//  organization.
	const client_org1 = Client.loadFromConfig('test/fixtures/network.yaml');
	const client_org2 = Client.loadFromConfig('test/fixtures/network.yaml');

	// Load the client information for an organization.
	// The file only has the client section.
	// A real application might do this when a new user logs in.
	client_org1.loadFromConfig('test/fixtures/org1.yaml');
	client_org2.loadFromConfig('test/fixtures/org2.yaml');

	try {
		// tell this client instance where the state and key stores are located
		await client_org1.initCredentialStores();

		// get the CA associated with this client's organization
		let caService = client_org1.getCertificateAuthority();

		let request = {
			enrollmentID: 'admin',
			enrollmentSecret: 'adminpw',
			profile: 'tls'
		};
		let enrollment = await caService.enroll(request);
		let key = enrollment.key.toBytes();
		let cert = enrollment.certificate;

		// set the material on the client to be used when building endpoints for the user
		client_org1.setTlsClientCertAndKey(cert, key);

		// tell this client instance where the state and key stores are located
		await client_org2.initCredentialStores();

		// get the CA associated with this client's organization
		caService = client_org2.getCertificateAuthority();
		t.equals(caService.fabricCAServices._fabricCAClient._caName, 'ca-org2', 'checking that caname is correct after resetting the config');
		request = {
			enrollmentID: 'admin',
			enrollmentSecret: 'adminpw',
			profile: 'tls'
		};
		enrollment = await caService.enroll(request);
		t.pass('Successfully called the CertificateAuthority to get the TLS material');
		key = enrollment.key.toBytes();
		cert = enrollment.certificate;

		// set the material on the client to be used when building endpoints for the user
		client_org2.setTlsClientCertAndKey(cert, key);
	}
