import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [book, setBook] = useState({ id: '', classificacao: '', comentario: '', infos_produto: '' });
  const [books, setBooks] = useState([]);
  const [backendURL, setBackendURL] = useState('https://kfficgz1id.execute-api.us-east-1.amazonaws.com/dev');

  // useEffect(() => {
  //   obterLivros()
  // }, []);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setBook((prevBook) => ({ ...prevBook, [name]: value }));
  };


  const handleURLChange = (event) => {
    setBackendURL(event.target.value);
  };

  const obterLivros = async () => {
      const response = await axios.get(`${backendURL}/feedback`);
      setBooks(response.data);
  }

  const cadastrar = async () => {
    try {
      const response = await axios.post(`${backendURL}/feedback`, book);

      if (response.status === 200 || response.status === 201) {
        // Atualize a lista local de livros após o cadastro
        setBooks([...books, response.data]);
        // Limpe o estado do livro atual
        setBook({ id: response.data.Item.id, classificacao: response.data.Item.classificacao, comentario: response.data.Item.comentario, infos_produto: response.data.Item.infos_produto});
      } else {
        // Trate outros códigos de status conforme necessário
        console.error("Erro ao cadastrar o livro", response.data);
      }

    }
    catch (error) {
      console.error("Erro ao conectar com o back-end", error);
    }
  };

  const atualizar = async (id) => {

  };

  const remover = async (id) => {
    const newBooks = books.filter(b => b.id !== id);
    setBooks(newBooks);


  };

  const obterLivro = async (id) => {
    try {
      const response = await axios.get(`${backendURL}/feedback/${id}`);
      console.log(response.status)
      if (response.status === 200) {
        setBook({ id: response.data.id, classificacao: response.data.classificacao, comentario: response.data.comentario, infos_produto: response.data.infos_produto });
        console.log(JSON.stringify(response.data))
      } else {
        console.error('Erro ao buscar livros')
      }

    }
    catch (error) {
      console.error("Erro ao conectar com o back-end", error);
    }
  };

  return (
    <div className="App">
      <form>
        <input
          name="id"
          placeholder="id"
          value={book.id}
          onChange={handleInputChange}
        />
        <input
          name="classificacao"
          placeholder="classificacao"
          value={book.classificacao}
          onChange={handleInputChange}
        />
        <input
          name="comentario"
          placeholder="comentario"
          value={book.comentario}
          onChange={handleInputChange}
        />
        <input
          name="infos_produto"
          placeholder="infos_produto"
          value={book.infos_produto}
          onChange={handleInputChange}
        />
        <button type="button" onClick={cadastrar}>Cadastrar</button>
        <button type="button" disabled onClick={() => atualizar(book.id)}>Atualizar</button>
        <button type="button" disabled onClick={() => remover(book.id)}>Remover</button>
        <button type="button" onClick={() => obterLivro(book.id)}>Obter pelo id</button>
        <button type="button" onClick={() => obterLivros()}>Obter todos</button>
      </form>
      <input
        className="backend-url-input"
        type="text"
        placeholder="URL do Backend"
        value={backendURL}
        onChange={handleURLChange}
      />
      <ul>
    {books.map(b => (
      <li key={b.id}>
        <div className="book-box">
          <div className="id">{b.id}</div>
          <div className="classificacao">{b.classificacao}</div>
          <div className="comentario">{b.comentario}</div>
        </div>
      </li>
    ))}
</ul>

    </div>
  );
}

export default App;
