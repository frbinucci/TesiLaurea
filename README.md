# TesiLaurea

In questo repository sono contenuti tutti gli script necessari alla messa in opera di un servizio di rete virtuale, mediante l'utilizzo dell'orchestratore OSM. Nella fattispecie, all'interno del pacchetto, vengono forniti dei flussi 
eseguibili mediante l'applicativo [KNIME](https://www.knime.com/). I suddetti flussi consentono, nella fattispecie, di compiere le seguenti operazioni:

* 1)Configurazione delle interfacce di rete su macchine con installato il sistema operativo Ubuntu 18.04 LTS (o versioni successive) a partire da un apposito file di configurazione definito dall'utente.
* 2)Generazione di file di configurazioni YAML (VNFD), atti alla messa in opera di un una VNF (Virtualized Network Function), a partire da un apposito file di configurazione definito dall'utente.
* 3)Generazione di file di configurazione YAML (NSD), atti alla messa in opera di un NS (Network Service), a partire da un apposito file di configurazione definito dall'utente.
* 4)Generazione di file di configurazione YAML, atti alla definizione di Network Slices, a partire da un apposito file di configurazione definito dall'utente.

## ISTRUZIONI DI UTILIZZO DEI FLUSSI

Una volta scaricato il repository occorre importare in KNIME il pacchetto contenente i vari flussi, contenuto all'interno della directory "flows" di questo repository. Il suddetto pacchetto, denominato "TesiLaurea", contiene due flussi:

* 1)Il primo contenente lo strumento necessario alla configurazione delle interfacce di rete in Ubuntu.
* 2)Il secondo, contenete tutti gli strumenti necessari al NFV (Network Functions Virtualization).

Si fa presente che i flussi generati si basano sull'utilizzo del linguaggio Python. Occorre, pertanto, che l'apposita estensione sia installata nella propria versione di KNIME.
Si rimanda alla apposita [sezione](https://www.knime.com/knime-software/knime-extensions) del sito ufficiale di KNIME per ulteriori informazioni sui componenti aggiuntivi.

I flussi necessari alla configurazione dei servizi di rete virtualizzati si avvalgono della libreria [ConfigObj](https://configobj.readthedocs.io/en/latest/configobj.html). Occorre pertanto che questa sia installata.

### ISTRUZIONI DI UTILIZZO DEL FLUSSO NECESSARIO ALLA CONFIGURAZIONE DELLE INTERFACCE DI RETE

In questa sezione si passa a descrivere il flusso utilizzato per la configurazione delle interfacce di rete in Linux Ubuntu 18.04.

#### PRIMA DI PROCEDERE

Per poter utilizzare il flusso generato occorre disabilitare la richiesta della password per l'esecuzione del comando sudo. Per fare ciò è sufficiente eseguire le seguenti operazioni:

* Aprire il terminare e digitare il comando sudo visudo.
* Aggiungere al file sudoers la seguente stringa: username ALL=(ALL) NOPASSWD:ALL

Si precisa che, ovviamente, al posto di "username" occorre indicare il proprio nome utente.

Il flusso consente di definire il file di input (contenente la configurazione desiderata) e il file di output (il file necessario alla configurazione delle interfacce di rete). 
Quest'ultimo file è presente al seguente percorso:

    /etc/netplan/50-cloud-init.yaml

N.B. Per poter utilizzare il flusso il file di destinazione deve essere già esistente!

#### ISTRUZIONI PER LA FORMATTAZIONE DEL FILE

Viene qui riportata, a titolo di esempio, la struttura del file di configurazione

    [enp0s3]
    configurazionev6 = false
    dhcp4 = false
    dhcp6 = false
    indirizzi = 192.168.1.1/24,FE80::4/10
    gateway = 192.168.1.1
    dns = 8.8.8.8

* Per ogni interfaccia occorre riportare il nome tra parentesi quadre.
* Il primo parametro specifica se si vuole o meno configurare un indirizzo IPv6 per l'interfaccia.
* Il secondo e il terzo parametro specificano se si vuole una configurazione basata su dhcp, sia per IPv4 che per IPv6.
* Il terzo parametro specifica gli indirizzi IPv4 e IPv6. Questi devono essere scritti nell'ordine mostrato, separati da virgola.
* Il quarto parametro specifica il gateway. Tale parametro è preso in considerazione solo in caso di configurazione IPv4 statica.
* L'ultimo parametro specifica una lista di server DNS. Si possono specificare più server DNS, a patto di separarli con la virgola.

#### ULTERIORI INFORMAZIONI

Non è necessario definire tutti i parametri precedentemente elencati. Inoltre l'ordine non è rilevante.

* Se non si specifica nulla circa la configurazione IPv6 questa viene, di default, disabilitata.
* Se non si specifica nulla circa i DHCP la configurazione si assume automaticamente statica.
* Se non si specifica alcun parametro di configurazione, si assume che si voglia configurare l'interfaccia come se fosse di strato 2. In tal caso viene ad essa assegnato un indirizzo IPv6 della classe link local.


#### ISTRUZIONI DI UTILIZZO DELLO SCRIPT "generate_configuration.py"

Viene messo a disposizione dell'utente anche un apposito script, denominato "generate_configuration.py", il quale fornisce una procedura guidata del file di configurazione. Il suddesso script riceve come
parametro il percorso del file di configurazione da esso generato. 
Nell'ipotesi in cui l'utente non specifichi alcun percorso, o specifichi un percorso non valido, lo script provvede a generare il file nella medesima directory su cui viene lanciato. Si consiglia di lanciare lo script
passando come parametro il percorso assoluto della directory ConfigurationFiles, posta all'interno della directory contenente il flusso KNIME.

### ISTRUZIONI DI UTILIZZO DEL FLUSSO RELATIVO ALLA CONFIGURAZIONE DEI SERVIZI DI RETE VIRTUALI

Si fa presente che, per quanto riguarda le procedure di importazione dei seguenti flussi, valgono le medesime considerazione fatte precedentemente per il flusso necessario alla configurazione delle interfacce di rete.

#### CONFIGURAZIONE DI UN VNF

Si riporta nel seguito un esempio di sintassi del file di configurazione necessario alla messa in opera di una VNF


    [Informazioni_Generali]
    id=hackfest-simplecharm-vnf
    nome=hackfest-simplecharm-vnf
    short=hackfest-simplecharm-vnf
    versione=1.0
    descrizione=A VNF consisting of 2 VDUs connected to an internal VL, and one VDU with cloud-init
    logo=osm.png

    [Punti_Connessione]
    [[vnf-mgmt]]
    nome=vnf-mgmt
    short=vnf-mgmt
    [[vnf-data]] 
    nome=vnf-data
    short=vnf-data

    [Link_Interno]
    [[internal]]
    nome=internal
    short=internal
    tipo=ELAN
    end_points=mgmtVM-internal,dataVM-internal

    [VDU]
    [[mgmtVM]]
    nome=mgmtVM
    immagine=hackfest3-mgmt
    num_progressivo=1
    [[[Caratteristiche_Hardware]]]
    num_cpu=1
    ram=1024
    capacita=10
    [[[Interfacce]]]
    [[[[mgmtVM-eth0]]]]
    posizione=1
    tipo=EXTERNAL
    end_point=vnf-mgmt
    [[[[mgmtVM-eth1]]]]
    posizione=2
    tipo=INTERNAL
    end_point=mgmtVM-internal
    [[[Punti_Connessione_Interni]]]
    [[[[mgmtVM-internal]]]]
    nome=mgmtVM-internal
    short=mgmtVM-internal

    [[dataVM]]
    nome=dataVM
    immagine=hackfest3-mgmt
    num_progressivo=1
    [[[Caratteristiche_Hardware]]]
    num_cpu=1
    ram=1024
    capacita=10

    [management] 
    interfaccia=vnf-mgmt


#### CONFIGURAZIONE DI UN NS

Si riporta nel seguito un esempio di file di configurazione necessarrio alla messa in opera di un NS

    [Info_Generali]
    id=hackfest_basic-ns
    nome=hackfest_basic-ns
    alias=hackfest_basic-ns
    descrizione=Simple NS with a single VNF and a single VL
    versione=1.0
    logo=osm.png

    [Lista_VNF]
    [[VNF1]]
    descrittore=hackfest_basic-vnf
    [[VNF2]]
    descrittore=hackfest_multivdu-vnf

    [VLD]
    [[mgmtnet]]
    nome=mgmtnet
    alias=mgmtnet
    tipo=ELAN
    management=true
    vim=mgmt
    [[[Punti_Connessione]]]
    [[[[Ref_1]]]]
    vnfd=hackfest_basic-vnf
    indice=1
    riferimento=vnf-cp0

#### CONFIGURAZIONE DI UNA NETWORK SLICE

Si riporta nel seguito un esempio di file di configurazione necessario alla messa in opera di una network slice

    [Informazioni_Generali]
    id=slice_hackfest_nst
    name=slice_hackfest_nst
    tipo_servizio=eMBB
    qos=1

    [subnet]
    [[slice_hackfest_nsd_1]]
    condivisa=false
    descrizione=NetSlice Subnet (service) composed by 2 vnfs and 4 cp (2 mgmt and 2 data)
    riferimento=slice_hackfest_nsd
    [[slice_hackfest_nsd_2]]
    condivisa=false
    descrizione=NetSlice Subnet (service) composed by 2 vnfs and 4 cp (2 mgmt and 2 data)
    riferimento=slice_hackfest_nsd

    [vld]
    [[slice_hackfest_vld_mgmt]]
    name=slice_hackfest_vld_mgmt
    tipo=ELAN
    management=true

    [[[punti_connessione]]]
    [[[[Ref_1]]]]
    nss=slice_hackfest_nsd_1
    punto=nsd_cp_mgmt

    [[[[Ref_2]]]]
    nss=slice_hackfest_nsd_2
    punto=nsd_cp_mgmt

    [[slice_hackfest_vld_data]]
    name=slice_hackfest_vld_mgmt
    tipo=ELAN

    [[[punti_connessione]]]
    [[[[Ref_1]]]]
    nss=slice_hackfest_nsd_1
    punto=nsd_cp_data

    [[[[Ref_2]]]]
    nss=slice_hackfest_nsd_2
    punto=nsd_cp_data
