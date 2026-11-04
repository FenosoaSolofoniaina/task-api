import { useState } from "react";

import { CustomH2MediumTitle } from "../components/Titles";

import { BodyLayout, AccountOption } from "../layouts/Body";
import { FooterLayout } from '../layouts/Footer';
import { HeaderLayout } from '../layouts/Header';
import { FormLayout } from "../layouts/Form";



function ForgotPasswordPage() {
    /*

    */

    const [identity, setIdentity] = useState('');

    const forgotPasswordFormStrucutres = [
        {
            format: "input",
            attributes : {
                id: "identity",
                type: "text",
                title: "Votre identifiant",
                value: identity,
                required: true,
                onChange: (e) => setIdentity(e.target.value),
            },
            text:"Identifiant *"
        },
        {
            format: "submit",
            attributes: {
                title: "Rechercher votre compte"
            },
            text: "Rechercher"
        }
    ];
    

    // ================================ HANDLE SUBMIT ================================ //
    async function searchIdentity(event) {
        /*
        
        */

        event.preventDefault();
        console.log(`Try to find account with identity "${identity}"`)

    }

    // ================================ RENDER ================================ //
    return (
        <> 
            <HeaderLayout />
            
            <BodyLayout>
                <CustomH2MediumTitle>
                    Mot de passe oublié ?
                </CustomH2MediumTitle>
                <FormLayout fields={forgotPasswordFormStrucutres}
                            onSubmit={searchIdentity} />
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


export default ForgotPasswordPage; 