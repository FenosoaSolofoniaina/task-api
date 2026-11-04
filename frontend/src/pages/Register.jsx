import { useState } from "react";

import { CustomH2MediumTitle } from "../components/Titles";

import { BodyLayout, AccountOption } from "../layouts/Body";
import { FooterLayout } from '../layouts/Footer';
import { HeaderLayout } from '../layouts/Header';
import { FormLayout } from "../layouts/Form";



function RegisterMePage() {
    /*

    */

    const [firstname, setFirstname] = useState('');
    const [lastname, setLastname] = useState('');
    const [sexe, setSexe] = useState("M");
    const [country, setCountry] = useState('Choisir votre pays...');
    const [dayBirth, setDayBirth] = useState("");

    const personalFormStructures = [
        {
            format: "input",
            attributes : {
                id: "firstname",
                type: "text",
                title: "Votre nom",
                value: firstname,
                required: true,
                onChange: (e) => setFirstname(e.target.value),
            },
            text:"Nom *"
        },
        {
            format: "input",
            attributes : {
                id: "lastname",
                type: "text",
                title: "Votre prénom",
                value: lastname,
                required: true,
                onChange: (e) => setLastname(e.target.value),
            },
            text:"Prénom *"
        },
        {
            format: "radio",
            group: {
                name: "sexe",
                items: [
                    {
                        attributes : {
                            id: "Homme",
                            value: "M",
                            checked: sexe === "M",
                            onChange: (e) => setSexe(e.target.value),
                        },
                        text: "Homme"
                    },
                    {
                        attributes : {
                            id: "Femme",
                            value: "F",
                            checked: sexe === "F",
                            onChange: (e) => setSexe(e.target.value),
                        },
                        text: "Femme"
                    }
                ],
            },
            text: "Genre"
        },
        {
            format: "input",
            attributes : {
                id: "birth",
                type: "date",
                title: "Votre date de naissance",
                value: dayBirth,
                required: true,
                onChange: (e) => setDayBirth(e.target.value),
            },
            text:"Date de naissance *"
        },
        {
            format: "select",
            attributes : {
                id: "country",
                onChange: (e) => setCountry(e.target.value),
            },
            options: ["Madagascar", "France", "Chine", "Australie", "Canada"],
            text:"Pays d'origine"
        },
        {
            format: "submit",
            attributes: {
                type: "submit",
                title: "Créér mon profil",
            },
            text: "Suivant"
        }
    ];
    

    // ================================ HANDLE SUBMIT ================================ //
    async function signup(event) {
        /*
        
        */

        event.preventDefault();
        console.log("Try to find sign up with informations :")
        console.log(firstname);
        console.log(lastname);
        console.log(sexe);
        console.log(dayBirth);
        console.log(country);

    }


    return (
        <> 
            <HeaderLayout />
            
            <BodyLayout>
                <CustomH2MediumTitle>
                    Créer un compte Task Manager
                </CustomH2MediumTitle>
                <AccountOption linkOption={
                    {
                        "href": '/login',
                        "text": "Se connecter"
                    }
                } >
                    Vous avez déjà un compte ?
                </AccountOption>
                <FormLayout fields={personalFormStructures}
                            onSubmit={signup} />
                <AccountOption linkOption={
                        {
                            "href": '/login',
                            "text": "Se connecter"
                        }
                    } >
                        Vous avez déjà un compte ?
                </AccountOption>
            </BodyLayout>

            <FooterLayout />
        </>
    );
}


export default RegisterMePage;