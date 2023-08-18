from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///orm_final_NT_GIT.db")
Base = declarative_base()


class Prisijungimai(Base):
    __tablename__ = "Prisijungimai"
    id = Column(Integer, primary_key=True)
    login = Column(String)
    passw = Column(String)


class Agenturos_NT(Base):
    __tablename__ = "Agenturos_NT"
    id = Column(Integer, primary_key=True)
    kaina_pardavimo = Column(Integer)
    kaina_nuoma = Column(Integer)
    Agenturos_id = Column(Integer, ForeignKey('agentura.id'))
    agent = relationship('Agentura', cascade="all, delete")
    NT_id = Column(Integer, ForeignKey('NT.id'))
    turtai = relationship('NT', cascade="all, delete")
    __table_args__ = (UniqueConstraint('Agenturos_id', 'NT_id'),)


class Agentura(Base):
    __tablename__ = "agentura"
    id = Column(Integer, primary_key=True)
    pavadinimas = Column(String)
    imones_kodas = Column(String)


class NT(Base):
    __tablename__ = 'NT'
    id = Column(Integer, primary_key=True)
    adresas = Column(String)
    plotas_kv_m = Column(Integer)
    registro_numeris = Column(String)

    Savininkai_id = Column(Integer, ForeignKey('savininkai.id'))
    savininkas = relationship('Savininkai', cascade="all, delete")


class Savininkai(Base):
    __tablename__ = "savininkai"
    id = Column(Integer, primary_key=True)
    vardas = Column(String)
    pavarde = Column(String)
    telefonas = Column(String)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# prisijungimas = Prisijungimai(login="tadas", passw="tadas")
# session.add(prisijungimas)
# session.commit()
# login_i = input("ivesk prisijungima:")
# passw_i = input("ivesk pass:")
# for pris in session.query(Prisijungimai).all():
#     if pris.login == login_i:
#         if pris.passw == passw_i:
#             pass
#         else:
#             print("Blogas pass")
#             exit()
#     else:
#         print("Blogas login")
#         exit()


while True:
    pasirinktis = input(
        "1. Ivesti pardaveja\n"
        "2. Ivesti agentura\n"
        "3. Priskirti agenturoms NT su kainomis\n"
        "4. NT paieska pagal miesta\n"
        "5. Paieska pagal miesta ir kainas\n"
        "6. Spausdinti viska\n")
    if pasirinktis == "q":
        print('iseinam is programos')
        break
    if pasirinktis == "1":
        pardavejas = Savininkai(vardas=input("Vardas:\n"), pavarde=input("Pavarde:\n"), telefonas=input("Telefonas:\n"))
        session.add(pardavejas)
        session.commit()
        pas = input("Ar nortie ivesti pardavejo NT ? T/N:\n")
        if pas == "T":
            while True:
                try:
                    turtas = NT(adresas=input("Iveskite NT adresa:\n"),
                                plotas_kv_m=int(input("Iveskite plota kv/m:\n")),
                                registro_numeris=input("Iveskite registro numeri:\n"), savininkas=pardavejas)
                except:
                    print("ivedete ne skaiciu")
                    continue
                session.add(turtas)
                session.commit()
                print("Sekmingai ivedete turta, ar norite ivesti dar viena turta ? T/N")
                pas2 = input("")
                if pas2 == "T":
                    continue
                else:
                    break
        else:
            continue

    if pasirinktis == "2":
        agentura_1 = Agentura(pavadinimas=input("Iveskite agenturos pavadinima"),
                              imones_kodas=input("Ivesktine imones koda"))
        session.add(agentura_1)
        session.commit()
    if pasirinktis == "3":
        while True:
            for agentura in session.query(Agentura).all():
                print(agentura.id, agentura.pavadinimas, agentura.imones_kodas)
            agent = int(input("Pire kokios agenturos priskirsite NT ? Iveskite ID numeri:\n"))

            agentura = session.query(Agentura).get(agent)

            for nt in session.query(NT).all():
                print(nt.id, nt.adresas, nt.plotas_kv_m, nt.registro_numeris)

            tur = int(input("Koki NT norite prijungti prie agenturos ? Iveskite ID numeri:\n")) ###################################################

            nt = session.query(NT).get(tur)


            sale = int(input("Kokia pardavimo kaina ?"))
            rent = int(input("Kokia nuomos kaina ?"))
            jungtis1 = Agenturos_NT(kaina_pardavimo=sale, kaina_nuoma=rent, agent=agentura, turtai=nt)
            session.add(jungtis1)
            session.commit()
            pas = input("Ar norite dar priskirti NT agenturoms ? T/N")
            if pas == "T":
                continue
            elif pas != "T":
                break
    if pasirinktis == "6":
        visi = session.query(Agenturos_NT).all()
        for viena in visi:
            print("Agentura: ", viena.agent.pavadinimas, "Pardavimo kaina: ", viena.kaina_pardavimo, "Nuomos kaina: ",
                  viena.kaina_nuoma, "NT adresas: ", viena.turtai.adresas, "Nt plotas: ",
                  viena.turtai.plotas_kv_m, "Savininkas: ", viena.turtai.savininkas.vardas,
                  viena.turtai.savininkas.pavarde)
    if pasirinktis == "4":
        miestas = input("Ivesk miesta pagal kuri iesktai NT")
        visi = session.query(Agenturos_NT).all()
        vidutine_kaina_l= []
        vidutine_nuoma_l = []
        for viena in visi:
            pad = (viena.turtai.adresas).split(" ")
            if miestas == pad[-1]:
                vidutine_kaina_l.append(viena.kaina_pardavimo)
                vidutine_nuoma_l.append(viena.kaina_nuoma)

                print("Agentura: ",viena.agent.pavadinimas, "Pardavimo kaina: ",viena.kaina_pardavimo,"Nuomos kaina: ",
                      viena.kaina_nuoma,"NT adresas: ", viena.turtai.adresas,"Nt plotas: ",
                      viena.turtai.plotas_kv_m,"Savininkas: ", viena.turtai.savininkas.vardas, viena.turtai.savininkas.pavarde)
        print("Vidutine pardavimo kaina", sum(vidutine_kaina_l)/len(vidutine_kaina_l))
        print("Vidutine nuomos kaina", sum(vidutine_nuoma_l) / len(vidutine_nuoma_l))

    if pasirinktis == "5":
        miestas = input("Ivesk miesta pagal kuri iesktai NT")
        nuo = int(input("Ivesnkite nuo kokios kainos ieskote"))
        iki = int(input("Ivesnkite iki kokios kainos ieskote"))
        visi = session.query(Agenturos_NT).all()
        vidutine_kaina_l = []
        vidutine_nuoma_l = []
        for viena in visi:
            pad = (viena.turtai.adresas).split(" ")
            kaina = viena.kaina_pardavimo
            if (miestas == pad[-1]) and  (kaina >= nuo) and (kaina <= iki):
                vidutine_kaina_l.append(viena.kaina_pardavimo)
                vidutine_nuoma_l.append(viena.kaina_nuoma)

                print("Agentura: ", viena.agent.pavadinimas, "Pardavimo kaina: ", viena.kaina_pardavimo,
                      "Nuomos kaina: ", viena.kaina_nuoma, "NT adresas: ", viena.turtai.adresas, "Nt plotas: ",
                      viena.turtai.plotas_kv_m, "Savininkas: ", viena.turtai.savininkas.vardas,
                      viena.turtai.savininkas.pavarde)
        print("Vidutine pardavimo kaina", sum(vidutine_kaina_l) / len(vidutine_kaina_l))
        print("Vidutine nuomos kaina", sum(vidutine_nuoma_l) / len(vidutine_nuoma_l))


        session.commit()
    # if pasirinktis == "2":
