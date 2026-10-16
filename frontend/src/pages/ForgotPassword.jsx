import { CustomBlueLink } from "../components/Ancres";
import { CustomBlueInput } from "../components/Inputs";
import { CustomBlueSubmitButton } from "../components/Buttons";
import { CustomH2MediumTitle } from "../components/Titles";



function ForgotPasswordForm({ forgotPasswordForms }) {

    return (
        <>
            {
                forgotPasswordForms.map(loginItem => <CustomBlueInput key={loginItem.id}
                                                                      id={loginItem.id}
                                                                      type={loginItem.type}
                                                                      placeholder={loginItem.placeholder}
                                                                      title={loginItem.title} >
                                                            {loginItem.text}
                                                        </CustomBlueInput>
                )
            }
        </>
    );
}


function BackToLoginForm() {

    const textLink = "connection";

    return (
        <div className="flex flex-row justify-center items-center m-y-[1em]" >
            <p>
                Retourner en page de
                <CustomBlueLink hrefLink="/login" 
                                title={textLink} >
                    {textLink}
                </CustomBlueLink>
            </p>
        </div>
    );
}


function ForgotPasswordPage() {

    function searchIdentity(event) {
        event.preventDefault();
        event.stopPropagation();

        alert('Searching...')
    }

    const forgotPasswordStructures = [
        {
            "id": "identity",
            "type": "text",
            "placeholder": "",
            "title": "Identifiant",
            "text": "Identifiant"
        }
    ];


    return (
        <div className="flex flex-row justify-center" >
            <div className="flex flex-col text-center border border-1 border-[#086288] rounded-[1em] bg-white w-[50%] p-[3em] gap-y-[2em]" >
                <CustomH2MediumTitle>
                    Chercher votre compte sur Task Manager App
                </CustomH2MediumTitle>
                <form method="POST" onSubmit={searchIdentity} >
                    <ForgotPasswordForm forgotPasswordForms={forgotPasswordStructures} />
                    <CustomBlueSubmitButton>
                        Rechercher
                    </CustomBlueSubmitButton>
                </form>
                <BackToLoginForm />
            </div>
        </div>
    );
}

export default ForgotPasswordPage; 