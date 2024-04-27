import Layout from "@/components/Layout";
import {useSession} from "next-auth/react";
import {useEffect, useState} from "react";
import Link from "next/link";
import ChipStatus from "@/components/dashboard/StatusChip";
import {Chip} from "@nextui-org/react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure} from "@nextui-org/react";
import {Input, Select, SelectItem} from "@nextui-org/react";
import {toast} from "react-toastify";
import {Spinner} from "@chakra-ui/react";

async function getListInputData(access_token: string) {
	const res = await fetch(process.env.API_URL + "ai/input/all/", {
		method: "get",
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	})
	return await res.json()
}


async function getInputDataDetails(access_token: string, inputDataId: string){
	const res = await fetch(process.env.API_URL + "ai/input/" + inputDataId, {
		method: "get",
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	})
	return await res.json()
}

async function getListResult(access_token: string, inputDataId: string){
	const res = await fetch(process.env.API_URL + "ai/result/" + inputDataId, {
		method: "get",
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	})
	return await res.json()
}


async function postResponse(access_token: string, inputDataId: string, result_type: string){
	const res = await fetch(process.env.API_URL + "ai/result/", {
		method: "post",
		headers: {
			Authorization: `Bearer ${access_token}`,
		 'Content-Type': 'application/json',
			'Accept': 'application/json'
		},
		body: JSON.stringify({
			input_id: inputDataId,
			result_type: result_type
		})
	})
	return await res.json();
}


const resultType: String[] = ["NOTE", "SUMMARY", "BULLETS", "LONG SUMMARY", "LONG NOTE"];
const languages = [
	{label: "English", value: "English", description: "English"},
	{label: "French", value: "French", description: "French"},
	{label: "German", value: "German", description: "German"},
	{label: "Italian", value: "Italian", description: "Italian"},
	{label: "Spanish", value: "Spanish", description: "Spanish"},
	{label: "Japanese", value: "Japanese", description: "Japanese"},
	{label: "Korean", value: "Korean", description: "Korean"},
	{label: "Danish", value: "Danish", description: "Danish"},
	{label: "Czech", value: "Czech", description: "Czech"},
	{label: "Dutch", value: "Dutch", description: "Dutch"},
	{label: "Polish", value: "Polish", description: "Polish"},
]

const aiTranscriptions = [
	{"label": "Generated", value: "GENERATED", description: "Generated"},
	{"label": "Manual", value: "MANUAL", description: "Manual"},
	{"label": "AI", value: "LLM", description: "AI"},

]


export default function Dashboard() {
	const {data: session, status} = useSession({required: true});

	const {isOpen, onOpen, onOpenChange} = useDisclosure();
	const [listInputData, setListInputData] = useState([]);
	const [detailInputData, setDetailInputData] = useState(null);
	const [listResult, setListResult] = useState([]);
	const [isLoading, setIsLoading] = useState(false);
	const [url, setUrl] = useState("");
	const [language, setLanguage] = useState("");
	const [transcription, setTranscription] = useState("");
	const [sidebarIsOpen, setSideBarIsOpen] = useState(false);

	const handleSubmitCreateInputData = async (e: any) => {
    e.preventDefault();

    setIsLoading(true);

    const formData = new FormData();
    formData.append("source_url", url);
    formData.append("language", language);
		formData.append("transcription_type", transcription);

    try {
      const response = await fetch(process.env.API_URL + "ai/input/", {
        method: "POST",
        headers: {
          accept: "application/json",
					Authorization: `Bearer ${session?.access_token}`
        },
        body: formData,
      });

			const res = await response.json();

      if (response.ok) {
        toast.success("Input data created successfully");
      } else {
        toast.error(res.detail);
      }
    } catch (error) {
      toast.error("Error while creating Input data object");
    } finally {
      setIsLoading(false);
    }
  };

	useEffect(() => {
		async function fetchData() {
			const data = await getListInputData(session?.access_token);
			setListInputData(data);
		}

		fetchData();
	}, [session?.access_token]);

	const handleListItemClick = async (inputDataId) => {
    const detailInputData = await getInputDataDetails(session?.access_token, inputDataId);
		setDetailInputData(detailInputData);

		const listResult = await getListResult(session?.access_token, inputDataId);
		setListResult(listResult);
  };

	const handleResponseCreate = async (inputDataId, resultType) => {
		if (!detailInputData){
			toast.error("Input data not found");
			return;
		}


		setIsLoading(true);
		const response = await postResponse(session?.access_token, inputDataId, resultType);

		const listResult = await getListResult(session?.access_token, inputDataId);
		setListResult(listResult);

		setIsLoading(false);
	}

  const toggleSidebar = () => {
    setSideBarIsOpen(!sidebarIsOpen);
  };


	if (status == "loading") {
    return <Spinner size="lg"/>;
  }

	if (session) {
		return (
			<>
				<Layout>
					<main className={"h-screen"}>
						{
							<>
								<button
									onClick={toggleSidebar} // Call toggleSidebar function on button click
									aria-controls="default-sidebar"
									type="button"
									className="inline-flex items-center p-2 mt-2 ms-3 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
								>
									<span className="sr-only">Toggle sidebar</span>
									<svg
										className="w-6 h-6"
										aria-hidden="true"
										fill="currentColor"
										viewBox="0 0 20 20"
										xmlns="http://www.w3.org/2000/svg"
									>
										<path
											clip-rule="evenodd"
											fill-rule="evenodd"
											d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"
										></path>
									</svg>
								</button>

								<aside
									id="default-sidebar"
									className={`fixed top-0 left-0 z-40 w-64 h-screen transition-transform ${
										sidebarIsOpen ? '' : '-translate-x-full'
									} sm:translate-x-0`}
									aria-label="Sidebar"
								>
									<div className="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800">
										<button
											onClick={toggleSidebar}
											className="absolute top-0 right-0 p-2 text-gray-500 hover:text-gray-600 focus:outline-none"
										>
											<span className="sr-only">Close sidebar</span>
											<svg
												className="w-6 h-6"
												fill="none"
												stroke="currentColor"
												viewBox="0 0 24 24"
												xmlns="http://www.w3.org/2000/svg"
											>
												<path
													strokeLinecap="round"
													strokeLinejoin="round"
													strokeWidth={2}
													d="M6 18L18 6M6 6l12 12"
												/>
											</svg>
										</button>
										<ul className="space-y-2 font-medium">

											<Button onPress={onOpen}>
												<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5"
														 stroke="currentColor" className="w-6 h-6">
													<path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15"/>
												</svg>
											</Button>
											<Modal backdrop={"blur"} isOpen={isOpen} onOpenChange={onOpenChange} isDismissable={false}
														 isKeyboardDismissDisabled={true}>
												<ModalContent>
													{(onClose) => (
														<>
															<ModalHeader className="flex flex-col gap-1">Process data</ModalHeader>
															<form onSubmit={handleSubmitCreateInputData}>
																<ModalBody>
																	<div className={"flex flex-col gap-2"}>
																		<div className="flex gap-2">
																			<div className="w-full">
																				<Input isRequired={true} type="url" label="Url"
																							 placeholder="Youtube/Spotify url"
																							 onChange={(e) => setUrl(e.target.value)}/>
																			</div>
																		</div>
																		<div className="flex gap-2">
																			<div className="w-full">
																				<Select
																					isRequired={true}
																					items={languages}
																					label="Language"
																					placeholder="Select a language"
																					onChange={(e) => setLanguage(e.target.value)}
																				>
																					{(language) => <SelectItem key={language.value}>{language.label}</SelectItem>}
																				</Select>
																			</div>
																			<div className="w-full">
																				<Select
																					isRequired={true}
																					items={aiTranscriptions}
																					label="Transcription type"
																					placeholder="Select a transcription type"
																					onChange={(e) => setTranscription(e.target.value)}
																				>
																					{(transcript) => <SelectItem
																						key={transcript.value}>{transcript.label}</SelectItem>}
																				</Select>
																			</div>
																		</div>
																	</div>
																</ModalBody>
																<ModalFooter>
																	<Button color="danger" variant="light" onPress={onClose}>
																		Close
																	</Button>
																	<Button type={"submit"} color="primary" onPress={onClose}>
																		Submit
																	</Button>
																</ModalFooter>
															</form>
														</>
													)}
												</ModalContent>
											</Modal>


											{Array.isArray(listInputData) && (
												listInputData.map((inputData) => (
													<li className={"hover:bg-gray-200 rounded-xl p-2 overflow-hidden overflow-ellipsis"}
															key={inputData?.id}>
														<Link href="#" onClick={() => handleListItemClick(inputData?.id)}>
															<div>
																<span className="flex-1 truncate">{inputData?.source_title}</span>
																<ChipStatus status={inputData?.status}/>
															</div>
														</Link>
													</li>
												))
											)}

										</ul>
									</div>
								</aside>

								<div className="p-4 sm:ml-64 flex flex-wrap h-[850px]">
									<>
										{detailInputData?.fragments.length > 0 && (
											<div className="w-full flex mb-4 gap-2">
												<Chip color={"default"}
															variant={"bordered"}>{detailInputData?.audio_length_minutes} minutes</Chip>
												<Chip color={"default"} variant={"bordered"}>{detailInputData?.language}</Chip>
												<Chip color={"default"} variant={"bordered"}>{detailInputData?.source}</Chip>
												<Chip color={"default"} variant={"bordered"}>{detailInputData?.transcription_type}</Chip>
											</div>
										)
										}
									</>

									<div
										className="p-4 w-1/2 border-2 flex-grow border-gray-200 border-solid rounded-lg dark:border-gray-700 overflow-y-auto"
										style={{maxHeight: "850px"}}>
										{detailInputData?.fragments.length > 0 && (
											detailInputData?.fragments.map((detail) => (
												<li key={detail?.id} className={"mb-5 list-none"}>
													<div>
														<Chip color={"default"} variant={"bordered"}>
															<strong>
																{detail.start_time.hours}:{detail.start_time.minutes}:{detail.start_time.seconds}
															</strong>
															-
															<strong>
																{detail.end_time.hours}:{detail.end_time.minutes}:{detail.end_time.seconds}
															</strong>
														</Chip>
														<p>{detail?.text}</p>
													</div>
												</li>
											))
										)}
									</div>
									<div
										className="p-4 w-1/2 border-2 flex-grow border-gray-200 border-solid rounded-lg dark:border-gray-700 overflow-y-auto"
										style={{maxHeight: "850px"}}>
										{Array.isArray(listResult) && (listResult.length > 0 && (
											listResult?.map((result) => (
												<li key={result?.id} className={"mb-5 list-none"}>
													<div>
														<Chip color={"default"} variant={"bordered"}>{result?.result_type}</Chip>
														<p>{result?.content}</p>
													</div>
												</li>
											))
										))}
									</div>

									{resultType.map((resultType, index) => (
										<div key={index} className={"mt-5 gap-2"}>
											<Button className={"mr-2"} variant={"ghost"} size={"sm"} isLoading={isLoading} type={"button"}
															onClick={() => handleResponseCreate(detailInputData?.id, resultType)}>
												{resultType}
											</Button>
										</div>
									))}
								</div>
							</>
						}
					</main>
				</Layout>
			</>
		);
	}

	return <></>;

}