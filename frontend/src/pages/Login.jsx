import { useRef, useEffect, useState } from "react";

import { CustomBlueLink } from "../components/Ancres";
import { CustomBlueInput } from "../components/Inputs";
import { CustomBlueSubmitButton } from "../components/Buttons";
import { CustomH2MediumTitle, CustomErrorTitle } from "../components/Titles";



function LoginForm({ loginError, loginForms, references, onSubmit }) {

    return (
        <form onSubmit={onSubmit} >
            {
                loginError && <LoginError />
            }
            {
                loginForms.map( (loginItem, index) => <CustomBlueInput
                            key={loginItem.id}
                            ref={references[index]}
                            id={loginItem.id}
                            type={loginItem.type}
                            placeholder={loginItem.placeholder}
                            title={loginItem.title}
                            required={loginItem.required} >
                        {loginItem.text}
                    </CustomBlueInput>
                )
            }
            <CustomBlueSubmitButton>
                Se connecter
            </CustomBlueSubmitButton>
        </form>
    );
}


function ForgotPassword() {

    const textLink = "Mot de passe oublié ?";

    return (
        <div className="flex flex-row justify-center items-center my-[0.3em]" >
            <CustomBlueLink hrefLink="/forgot-password"
                            title={textLink} >
                {textLink}
            </CustomBlueLink>
        </div>
    );
}


function CreateNewAccount() {

    const textLink = "Créér un nouveau compte";

    return (
        <div className="flex flex-row justify-center items-center my-[0.3em]" >
            <p>
                Vous n'avez pas encore de compte ?  
            </p>
            <CustomBlueLink hrefLink="/register" 
                            title={textLink} >
                {textLink}
            </CustomBlueLink>
        </div>
    );
}


function LoginError() {

    return (
        <CustomErrorTitle >
            Identifiant ou mot de passe incorrecte
        </CustomErrorTitle>
    );
}


function LoginPage() {

    // ================================ USES ================================ //
    const identityRef = useRef(null);
    const passwordRef = useRef(null);
    const [loginFormStructure, setLoginFormStructure] = useState(null);
    const [hasLoginError, setHasLoginError] = useState(false);

    // ================================ HANDLE SUBMIT ================================ //
    async function sendLoginForm(event) {

        event.preventDefault();

        const endPointUrl = 'http://localhost:8000/login/auth';
        
        try {
            const response = await fetch(
                endPointUrl,
                {
                    method:"POST",
                    body: JSON.stringify({
                        "identity": identityRef.current.value,
                        "password": passwordRef.current.value
                    }),
                    headers: { 'Content-Type': 'application/json' }
                }
            );
            if(!response.ok) {
                throw new Error(`HTTP error: Failed to send request from "${endPointUrl}"`);
            }
            const authData = await response.json();
            setHasLoginError(!authData.authenticate)
        }
        catch (err) { console.error(err) }

    }


    // ================================ BUILD LOGIN INPUTS ================================ //
    useEffect( () => {

        async function builLoginForm() {
        
            const endPointUrl = 'http://localhost:8000/login/forms';
            try {
                const response = await fetch(endPointUrl);
                if(!response.ok) {
                    throw new Error(`HTTP error: Failed to send request from "${endPointUrl}"`);
                }
                setLoginFormStructure(await response.json());
            }
            catch (err) { console.error(err) }
        }

        builLoginForm();

    }, []);    

    // ================================ RENDER ================================ //
    return (
        <div className="flex flex-row justify-center" >
            <div className="flex flex-col text-center border border-1 border-[#086288] rounded-[1em] bg-white w-[50%] p-[3em] gap-y-[2em]" >
                <CustomH2MediumTitle>
                    Se connecter à Task Manager App
                    </CustomH2MediumTitle>
                {
                    loginFormStructure &&
                    <>
                        <LoginForm loginForms={loginFormStructure}
                                loginError={hasLoginError}
                                references={[identityRef, passwordRef]}
                                onSubmit={sendLoginForm} />
                    </>
                }
                <ForgotPassword />
                <CreateNewAccount />
            </div>
        </div>
    );
}


export default LoginPage; 