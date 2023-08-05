Plaster
=======

Project to bring similar functionality found in Rails to the Spring Boot
platform. Currently only supports maven-enabled projects.

For Example:

::

    plaster g scaffold User name:string age:integer

Will create the following files:

- Model - root/model/User.java
- Repository - root/repository/UserRepository.java
- Service - service/UserService.java
- Controller - controller/UsersController.java

The root is calculated upon script start. For example, if being run on a
project with the following in `pom.xml`:

::

    <groupId>com.example</groupId>

the root will be `src/main/com/example/`

Installation
""""""""""""

If you have `pip <https://pip.pypa.io/en/stable/installing/>`__
installed, you can install Plaster with following:

::

    pip install plaster-spring-boot

Otherwise, ensure Python's `setuptools` is installed to install
Plaster. If on an ubuntu system, use the following:

::

    sudo apt-get install python-setuptools

Otherwise, explore
`setuptools <https://pypi.python.org/pypi/setuptools>`__ to find how to
install for your system. Then download Plaster onto your machine,
navigate to the directory in which it was downloaded and run:

::

    python setup.py install

Usage
"""""

::

    usage: plaster [-h] [-v] [-k [KEY]] [-d DIR]
                   {generate,g,delete,d}
                   {scaffold,model,repository,service,controller,field} model_name
                   [fields [fields ...]]

    Generate files for Spring Boot

    positional arguments:
      {generate,g,delete,d}
                            whether to generate or delete
                                generate, g - create files
                                delete, d - remove files
      {scaffold,model,repository,service,controller,field}
                            how to generate or delete content
                                scaffold - all files associated to the model
                                model - the entire model
                                repository - the entire repository
                                service - the entire service
                                controller - the entire controller
                                field - individual field(s)
      model_name            name of model for which to perform actions
      fields                fields to perform actions listed as name:type pairs

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         fetches the current version of the tool
      -k [KEY], --key [KEY]
                            indicates the following field:type pair should define the key
                            NOTE: should be a trailing param
      -d DIR, --dir DIR     defines a sub path in which to perform actions
                            NOTE: should be a trailing param

Customization
"""""""""""""

Per default, Plater will auto-discover necessary configurations and then
use best-practices to decide where and how to generate files. However,
if you would like to customize the generation of the files, Plater gives
you the ability to alter defaults by placing `plaster.yml` in the root
of the project. The following configurations are supported:

Property `dir`
^^^^^^^^^^^^^^

+--------------+-----------------------------------------------+----------+--------------+
| Property     | Description                                   | Type     | Default      |
+==============+===============================================+==========+==============+
| model        | Directory in which to generate models         | String   | model        |
+--------------+-----------------------------------------------+----------+--------------+
| repository   | Directory in which to generate repositories   | String   | repository   |
+--------------+-----------------------------------------------+----------+--------------+
| controller   | Directory in which to generate controllers    | String   | controller   |
+--------------+-----------------------------------------------+----------+--------------+
| service      | Directory in which to generate services       | String   | service      |
+--------------+-----------------------------------------------+----------+--------------+

Property `lombok`
^^^^^^^^^^^^^^^^^

+----------------+-----------------------------------------+---------+-----------+
| Property       | Description                             | Type    | Default   |
+================+=========================================+=========+===========+
| enabled        | Should we enable generation in lombok   | Boolean | Is lombok |
|                | mode                                    |         | a         |
|                |                                         |         | dependenc |
|                |                                         |         | y         |
|                |                                         |         | in        |
|                |                                         |         | `pom.xml` |
|                |                                         |         | ?         |
+----------------+-----------------------------------------+---------+-----------+

Lombok Support
""""""""""""""

Generation of models will change if a lombok dependency is found in
`pom.xml`. This will import lombok and annotate the model differently.
For example:

::

    //NO LOMBOK
    @Entity
    public class Example {

        @Id
        @GeneratedValue(strategy = GenerationType.AUTO)
        private Integer id;

        public Integer getId() {
            return this.id;
        }

        public void setId(Integer id) {
            this.id = id;
        }

    }


::

    import lombok.AllArgsConstructor;
    import lombok.Builder;
    import lombok.Data;
    import lombok.NoArgsConstructor;

    @AllArgsConstructor
    @Builder
    @Data
    @NoArgsConstructor
    public class Example {

        @Id
        @GeneratedValue(strategy = GenerationType.AUTO)
        private Integer id;

    }

For lombok information, visit the project's
`homepage <https://projectlombok.org/>`__.