# TesiLaurea

Questo repository contiene tutti gli script necessari al funzionamento di un flusso KNIME utile alla configurazione di un servizio di rete virtuale. 
Allo stato attuale sono state implementate le seguenti funzionalità:

1)Configurazione delle interfacce di rete mediante il file "50-cloud-init.yaml" sul sistema operativo Ubuntu 18.04
2)Configurazione del descrittore relativo ad una VNF (Virtualized Network Function) (funzionalità da migliorare).

## ISTRUZIONI DI UTILIZZO DEL FLUSSO RELATIVO ALLA CONFIGURAZIONE DELLE INTERFACCE DI RETE

Per poter testare l'applicativo è necessario avere installato KNIME. All'interno della cartella "flows" è presente il file contenente il pacchetto dei flussi.
Una volta importato il flusso, per testarne il funzionamento, è necessario recarsi nella directory "ConfigurationFiles", posta all'interno della directory del flusso.
All'interno di tale cartella è presente un file, chiamato "config.cfg", nel quale viene fornita la configurazione dell'interfaccia di rete.

### PRIMA DI PROCEDERE

Per poter utilizzare il flusso generato occorre disabilitare la richiesta della password per l'esecuzione del comando sudo. Per fare ciò è sufficiente eseguire le seguenti operazioni:

* Aprire il terminare e digitare il comando sudo visudo.
* Aggiungere al file sudoers la seguente stringa: username ALL=(ALL) NOPASSWD:ALL

Si precisa che, ovviamente, al posto di "username" occorre indicare il proprio nome utente.


### ISTRUZIONI PER LA FORMATTAZIONE DEL FILE

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

### ULTERIORI INFORMAZIONI

Non è necessario definire tutti i parametri precedentemente elencati. Inoltre l'ordine non è rilevante.

* Se non si specifica nulla circa la configurazione IPv6 questa viene, di default, disabilitata.
* Se non si specifica nulla circa i DHCP la configurazione si assume automaticamente statica.
* Se non si specifica alcun parametro di configurazione, si assume che si voglia configurare l'interfaccia come se fosse di strato 2. In tal caso viene ad essa assegnato un indirizzo IPv6 della classe link local.


### ISTRUZIONI DI UTILIZZO DELLO SCRIPT "generate_configuration.py"

Viene messo a disposizione dell'utente anche un apposito script, denominato "generate_configuration.py", il quale fornisce una procedura guidata del file di configurazione. Il suddesso script riceve come
parametro il percorso del file di configurazione da esso generato. 
Nell'ipotesi in cui l'utente non specifichi alcun percorso, o specifichi un percorso non valido, lo script provvede a generare il file nella medesima directory su cui viene lanciato. Si consiglia di lanciare lo script
passando come parametro il percorso assoluto della directory ConfigurationFiles, posta all'interno della directory contenente il flusso KNIME.

## ISTRUZIONI DI UTILIZZO DEL FLUSSO RELATIVO ALLA CONFIGURAZIONE DEI SERVIZI DI RETE VIRTUALI

Questo flusso è ancora in fase di costruzione. Maggiori informazioni saranno fornite non appena le funzionalità salienti saranno implementate.

### CONFIGURAZIONE DI UN VNFD

Under Construction...

### CONFIGURAZIONE DI UN NSD

Under Construction...

