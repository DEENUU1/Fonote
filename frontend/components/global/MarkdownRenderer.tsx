import ReactMarkdown from "react-markdown";


const MarkdownRenderer = ({markdown}: { markdown: string }) => {
	return (
		<div className="prose">
			<ReactMarkdown>{markdown}</ReactMarkdown>
		</div>
	);
};


export default MarkdownRenderer;
